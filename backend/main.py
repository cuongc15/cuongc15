from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, ForeignKey, Numeric, String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from backend.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, future=True)


class Base(DeclarativeBase):
    pass


class Classroom(Base):
    __tablename__ = "classrooms_demo"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)


class Assignment(Base):
    __tablename__ = "assignments_demo"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    class_id: Mapped[str] = mapped_column(ForeignKey("classrooms_demo.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)


class Grade(Base):
    __tablename__ = "grades_demo"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    class_id: Mapped[str] = mapped_column(ForeignKey("classrooms_demo.id", ondelete="CASCADE"), nullable=False)
    assignment_id: Mapped[str] = mapped_column(ForeignKey("assignments_demo.id", ondelete="CASCADE"), nullable=False)
    student_name: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ClassroomIn(BaseModel):
    name: str = Field(min_length=1)
    subject: str = Field(min_length=1)


class AssignmentIn(BaseModel):
    class_id: str
    title: str = Field(min_length=1)
    due_at: datetime


class GradeIn(BaseModel):
    assignment_id: str
    student_name: str = Field(min_length=1)
    score: float = Field(ge=0, le=10)


app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    try:
        Base.metadata.create_all(engine)
    except Exception as exc:
        # Không crash service chỉ vì DB tạm thời chưa sẵn sàng trên Railway.
        print(f"[startup] database init skipped: {exc}")


@app.get("/health")
def health():
    db_ok = True
    db_error = None
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        db_ok = False
        db_error = str(exc)

    return {"status": "ok", "env": settings.app_env, "db_ok": db_ok, "db_error": db_error}


@app.get("/api/classes")
def list_classes():
    with Session(engine) as s:
        rows = s.scalars(select(Classroom).order_by(Classroom.name)).all()
        return [{"id": r.id, "name": r.name, "subject": r.subject} for r in rows]


@app.post("/api/classes")
def create_class(payload: ClassroomIn):
    with Session(engine) as s:
        row = Classroom(name=payload.name.strip(), subject=payload.subject.strip())
        s.add(row)
        s.commit()
        return {"id": row.id, "name": row.name, "subject": row.subject}


@app.delete("/api/classes/{class_id}")
def delete_class(class_id: str):
    with Session(engine) as s:
        c = s.get(Classroom, class_id)
        if not c:
            raise HTTPException(404, "Class not found")
        s.query(Grade).filter(Grade.class_id == class_id).delete()
        s.query(Assignment).filter(Assignment.class_id == class_id).delete()
        s.delete(c)
        s.commit()
        return {"ok": True}


@app.get("/api/assignments")
def list_assignments():
    with Session(engine) as s:
        rows = s.scalars(select(Assignment).order_by(Assignment.due_at.desc())).all()
        return [{"id": r.id, "classId": r.class_id, "title": r.title, "dueAt": r.due_at.isoformat()} for r in rows]


@app.post("/api/assignments")
def create_assignment(payload: AssignmentIn):
    with Session(engine) as s:
        if not s.get(Classroom, payload.class_id):
            raise HTTPException(400, "Invalid class")
        row = Assignment(class_id=payload.class_id, title=payload.title.strip(), due_at=payload.due_at)
        s.add(row)
        s.commit()
        return {"id": row.id, "classId": row.class_id, "title": row.title, "dueAt": row.due_at.isoformat()}


@app.delete("/api/assignments/{assignment_id}")
def delete_assignment(assignment_id: str):
    with Session(engine) as s:
        a = s.get(Assignment, assignment_id)
        if not a:
            raise HTTPException(404, "Assignment not found")
        s.query(Grade).filter(Grade.assignment_id == assignment_id).delete()
        s.delete(a)
        s.commit()
        return {"ok": True}


@app.get("/api/grades")
def list_grades(class_id: Optional[str] = None):
    with Session(engine) as s:
        stmt = select(Grade)
        if class_id:
            stmt = stmt.where(Grade.class_id == class_id)
        rows = s.scalars(stmt.order_by(Grade.created_at.desc())).all()
        items = [
            {
                "id": r.id,
                "classId": r.class_id,
                "assignmentId": r.assignment_id,
                "studentName": r.student_name,
                "score": f"{float(r.score):.2f}",
            }
            for r in rows
        ]
        avg = round(sum(float(x["score"]) for x in items) / len(items), 2) if items else 0
        return {"items": items, "avg": avg}


@app.post("/api/grades")
def create_grade(payload: GradeIn):
    with Session(engine) as s:
        a = s.get(Assignment, payload.assignment_id)
        if not a:
            raise HTTPException(400, "Invalid assignment")
        row = Grade(
            class_id=a.class_id,
            assignment_id=payload.assignment_id,
            student_name=payload.student_name.strip(),
            score=payload.score,
        )
        s.add(row)
        s.commit()
        return {"id": row.id}


@app.delete("/api/grades/{grade_id}")
def delete_grade(grade_id: str):
    with Session(engine) as s:
        g = s.get(Grade, grade_id)
        if not g:
            raise HTTPException(404, "Grade not found")
        s.delete(g)
        s.commit()
        return {"ok": True}


@app.post("/api/seed")
def seed_data():
    with Session(engine) as s:
        s.query(Grade).delete()
        s.query(Assignment).delete()
        s.query(Classroom).delete()
        c1 = Classroom(name="10A1 Toán", subject="Toán học")
        c2 = Classroom(name="11B2 Anh văn", subject="Tiếng Anh")
        s.add_all([c1, c2])
        s.flush()
        a1 = Assignment(class_id=c1.id, title="Kiểm tra chương 1", due_at=datetime.utcnow())
        s.add(a1)
        s.commit()
        return {"ok": True}


@app.delete("/api/reset")
def reset_all():
    with Session(engine) as s:
        s.query(Grade).delete()
        s.query(Assignment).delete()
        s.query(Classroom).delete()
        s.commit()
    return {"ok": True}

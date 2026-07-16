"""High School Management System API backed by a SQLite database."""

from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

try:
    from .database import Base, engine, get_db
    from .models import Activity, Registration, User
    from .seed_data import seed_database
except ImportError:  # pragma: no cover - fallback for direct execution
    from database import Base, engine, get_db
    from models import Activity, Registration, User
    from seed_data import seed_database

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    seed_database()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    activities = db.scalars(
        select(Activity)
        .options(selectinload(Activity.registrations))
        .order_by(Activity.name)
    ).all()

    return {activity.name: serialize_activity(activity) for activity in activities}


def serialize_activity(activity: Activity) -> dict:
    return {
        "description": activity.description,
        "schedule": activity.schedule,
        "max_participants": activity.max_participants,
        "participants": [registration.email for registration in activity.registrations],
    }


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    activity = db.get(Activity, activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if any(registration.email == email for registration in activity.registrations):
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    if len(activity.registrations) >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    if db.get(User, email) is None:
        db.add(User(email=email))

    db.add(Registration(activity_name=activity_name, email=email))
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    activity = db.get(Activity, activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    registration = db.scalar(
        select(Registration).where(
            Registration.activity_name == activity_name,
            Registration.email == email,
        )
    )
    if registration is None:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    db.delete(registration)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}

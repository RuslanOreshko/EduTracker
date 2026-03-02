from edutracker.infrastructure.db.teacher_catalog.base import TeacherBase
from edutracker.infrastructure.db.teacher_catalog.session import engine

from edutracker.infrastructure.db.teacher_catalog import model



def main() -> None:
    TeacherBase.metadata.create_all(engine)
    print()


if __name__ == "__main__":
    main()
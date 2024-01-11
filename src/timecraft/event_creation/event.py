


@dataclass(slots=True)
class Event:
    classes: List[Class]
    no_hours: int
    student_group: str
    fixed_slots: Optional[List[int]] = None
    _course_codes: Optional[List[str]] = None
    _faculty_codes: Optional[List[str]] = None

    @property
    def course_codes(self):
        if not self._course_codes:
            self._course_codes = [c.course.code for c in self.classes]
        return self._course_codes

    @property
    def faculty_codes(self):
        if not self._faculty_codes:
            self._faculty_codes = []
            for c in self.classes:
                self._faculty_codes += c.faculty_codes
        return self._faculty_codes
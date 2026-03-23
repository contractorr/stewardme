"""SM-2 spaced repetition algorithm."""

from dataclasses import dataclass


@dataclass
class SM2Result:
    easiness_factor: float
    interval_days: int
    repetitions: int


def sm2_update(
    easiness_factor: float,
    interval_days: int,
    repetitions: int,
    grade: int,
) -> SM2Result:
    """Compute next SM-2 scheduling values.

    Args:
        easiness_factor: Current EF (>= 1.3).
        interval_days: Current interval in days.
        repetitions: Number of successful repetitions.
        grade: Quality grade 0-5 (0=blackout, 5=perfect).

    Returns:
        SM2Result with updated values.
    """
    grade = max(0, min(5, grade))

    # Update easiness factor
    new_ef = easiness_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    new_ef = max(1.3, new_ef)

    if grade < 3:
        # Failed — reset repetitions, short interval
        return SM2Result(
            easiness_factor=new_ef,
            interval_days=1,
            repetitions=0,
        )

    # Successful recall
    new_reps = repetitions + 1
    if new_reps == 1:
        new_interval = 1
    elif new_reps == 2:
        new_interval = 6
    else:
        new_interval = round(interval_days * new_ef)

    return SM2Result(
        easiness_factor=new_ef,
        interval_days=max(1, new_interval),
        repetitions=new_reps,
    )

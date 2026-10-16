
"""A simple election system demonstrating code-quality improvements."""

import secrets
import xml.etree.ElementTree as ET
from datetime import datetime

POLLS_CLOSE_HOUR = 18
VOTERS = {}
BALLOTS = []
CANDIDATES = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id, name, age):
    """Register a voter who meets the minimum age requirement."""
    if age < 18 or voter_id in VOTERS:
        return False

    VOTERS[voter_id] = {"name": name, "voted": False}
    return True


def is_officer(role):
    """Check whether a person has the election officer role."""
    return role == "election_officer"


def cast_vote(voter_id, candidate, when):
    """Record one valid vote before polling closes."""
    if voter_id not in VOTERS:
        return False

    if VOTERS[voter_id]["voted"]:
        return False

    if when.hour >= POLLS_CLOSE_HOUR:
        return False

    valid_candidate = next(
        (name for name in CANDIDATES
         if name.casefold() == candidate.casefold()),
        None,
    )
    if valid_candidate is None:
        return False

    BALLOTS.append(valid_candidate)
    VOTERS[voter_id]["voted"] = True
    return True


def tally():
    """Return the number of votes for each candidate."""
    counts = {name: 0 for name in CANDIDATES}
    for candidate in BALLOTS:
        counts[candidate] += 1
    return counts


def winner():
    """Return the candidate with the most votes, or None if no votes."""
    counts = tally()
    if not BALLOTS:
        return None
    return max(counts, key=counts.get)


def vote_percent(candidate):
    """Calculate a candidate's percentage of recorded ballots."""
    if not BALLOTS:
        return 0
    return tally().get(candidate, 0) * 100 / len(BALLOTS)


def turnout():
    """Calculate turnout as a percentage of registered voters."""
    if not VOTERS:
        return 0
    return len(BALLOTS) / len(VOTERS) * 100


def count_for(candidate, ballot_list):
    """Count ballots for a particular candidate."""
    return sum(ballot == candidate for ballot in ballot_list)


def announce():
    """Return vote-count announcements for all candidates."""
    counts = tally()
    return [
        f"{name}: {counts[name]}"
        for name in CANDIDATES
    ]


def receipt_number():
    """Generate a six-digit receipt number."""
    return f"RCPT-{secrets.randbelow(900000) + 100000}"


def import_postal_ballots(xml_text):
    """Import ballots with valid candidate names from XML."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return 0

    imported = 0
    for ballot in root.iter("ballot"):
        candidate = ballot.get("candidate", "")
        valid_candidate = next(
            (name for name in CANDIDATES
             if name.casefold() == candidate.casefold()),
            None,
        )
        if valid_candidate is not None:
            BALLOTS.append(valid_candidate)
            imported += 1

    return imported


def main():
    """Run demonstration tests and display election results."""
    print("Register Asha (age 18):",
          register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)

    print("Is a plain 'voter' an election officer:",
          is_officer("voter"))
    print("Ben votes Alice:",
          cast_vote("V2", "Alice", datetime(2026, 11, 20, 10, 0)))
    print("Ben votes Alice again:",
          cast_vote("V2", "Alice", datetime(2026, 11, 20, 11, 0)))
    print("Chen votes 'bob':",
          cast_vote("V3", "bob", datetime(2026, 11, 20, 12, 0)))
    print("Dia votes Bob at 18:30:",
          cast_vote("V4", "Bob", datetime(2026, 11, 20, 18, 30)))

    postal_xml = (
        "<postal><ballot voter='V1' candidate='Bob'/></postal>"
    )
    print("Postal ballots imported:",
          import_postal_ballots(postal_xml))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()

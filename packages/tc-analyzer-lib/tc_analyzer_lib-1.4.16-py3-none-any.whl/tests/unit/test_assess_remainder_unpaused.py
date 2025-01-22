from tc_analyzer_lib.algorithms.assessment.assess_remainder import assess_remainder


def test_assess_unpaused():
    all_active = {
        "0": set(["user0", "user1", "user2", "user3", "user4"]),
        "1": set(["user0", "user1", "user2", "user3"]),
        "2": set(["user0", "user1", "user2", "user3", "user5"]),
    }

    all_new_active = {
        "0": set(["user0", "user1", "user2", "user3", "user4"]),
        "1": set([]),
    }
    all_unpaused = {
        "0": set([]),
        "1": set([]),
    }
    all_returned = {
        "0": set([]),
        "1": set([]),
    }
    all_paused = {
        "0": set([]),
        "1": set(["user5"]),
    }
    all_disengaged = {
        "0": set([]),
        "1": set([]),
    }
    all_disengaged_in_past = {
        "0": set([]),
        "1": set([]),
    }
    all_new_disengaged = {
        "0": set([]),
        "1": set([]),
    }

    (
        all_new_active,
        all_unpaused,
        all_returned,
        all_paused,
        all_new_disengaged,
        all_disengaged,
        all_disengaged_in_past,
    ) = assess_remainder(
        all_active=all_active,
        w_i=2,
        WINDOW_D=1,
        PAUSED_T_THR=1,
        all_new_active=all_new_active,
        all_unpaused=all_unpaused,
        all_returned=all_returned,
        all_paused=all_paused,
        all_disengaged=all_disengaged,
        all_disengaged_in_past=all_disengaged_in_past,
        all_new_disengaged=all_new_disengaged,
    )

    assert all_paused["2"] == set([])
    assert all_unpaused["2"] == set(["user5"])
    assert all_returned["2"] == set([])
    assert all_new_disengaged["2"] == set([])
    assert all_disengaged_in_past["2"] == set([])

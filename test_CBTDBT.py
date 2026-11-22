import pytest
import json
import os
import re
from unittest.mock import patch, MagicMock

os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

# FIX: Import from the actual modules where classes/functions live,
#      not all from app. This was causing import errors and masking
#      the real patching targets.
from data_manager import load_data, save_data
from home_screen import HomeScreen
from cbt_screens import (
    CBTThoughtScreen, CBTActivityScreen, CBTCopingScreen, CBTValuesScreen
)
from dbt_screens import DBTDiaryScreen, DBTDEARMANScreen, DBTOppositeScreen
from soothe_screens import SootheSensesScreen
from tools_screens import (
    ToolsMoodScreen, ToolsGratitudeScreen, ToolsHabitsScreen, ToolsSafetyScreen
)


def strip_kivy_markup(text):
    return re.sub(r'\[.*?\]', '', text)


@pytest.fixture
def data_file(tmp_path, monkeypatch):
    """Create a temp data file and monkeypatch DATA_FILE in data_manager."""
    file_path = tmp_path / "test_data.json"
    # FIX: Must patch in data_manager because that's where load_data/save_data look it up
    monkeypatch.setattr("data_manager.DATA_FILE", str(file_path))
    return file_path


@pytest.fixture
def mock_popup():
    """Mock show_popup across all modules that import it."""
    # FIX: Patch in every module that uses it, otherwise the local
    #      name reference won't be patched.
    with patch("data_manager.show_popup") as dm_p, \
         patch("cbt_screens.show_popup") as cbt_p, \
         patch("dbt_screens.show_popup") as dbt_p, \
         patch("soothe_screens.show_popup") as soothe_p, \
         patch("tools_screens.show_popup") as tools_p:
        yield dm_p  # yield one representative mock for assertions


def test_load_save_data(data_file):
    initial_data = load_data()
    assert initial_data["moods"] == []
    initial_data["moods"].append({"mood": 8, "time": "2023-10-01"})
    save_data(initial_data)
    loaded_data = load_data()
    assert len(loaded_data["moods"]) == 1
    assert loaded_data["moods"][0]["mood"] == 8


def test_home_screen_insights(data_file, mock_popup):
    data = load_data()
    data["moods"] = [{"mood": 4}, {"mood": 6}]
    data["thoughts"] = [{"situation": "Test"}]
    save_data(data)
    screen = HomeScreen()
    screen.update_insights()
    plain = strip_kivy_markup(screen.insights_label.text)
    assert "5.0" in plain
    assert "Thought Records: 1" in plain


def test_cbt_thought_record(data_file, mock_popup):
    screen = CBTThoughtScreen()
    screen.in_sit.text = "Test Situation"
    screen.in_tho.text = "Test Thought"
    screen.spin.text = "Catastrophizing"
    screen.in_rat.text = "Test Rational"
    screen.save_thought()
    data = load_data()
    assert len(data["thoughts"]) == 1
    assert data["thoughts"][0]["situation"] == "Test Situation"
    assert data["thoughts"][0]["distortion"] == "Catastrophizing"


def test_cbt_activity(data_file, mock_popup):
    screen = CBTActivityScreen()
    screen.in_act.text = "Went for a walk"
    screen.in_mast.text = "8"
    screen.in_pleas.text = "7"
    screen.save_act()
    data = load_data()
    assert len(data["activities"]) == 1
    assert data["activities"][0]["mastery"] == 8
    assert data["activities"][0]["pleasure"] == 7


def test_cbt_coping_cards(data_file, mock_popup):
    screen = CBTCopingScreen()
    # Screen loads first default card
    assert screen.lbl_card.text == "I can handle this."
    # Add a new card
    screen.in_new.text = "I am resilient"
    screen.add_card()
    data = load_data()
    assert "I am resilient" in data["coping_cards"]
    # add_card displays the newly added card
    assert screen.lbl_card.text == "I am resilient"
    # next_card(1) wraps from idx=2 back to idx=0
    screen.next_card(1)
    assert screen.lbl_card.text == "I can handle this."
    # Continue cycling
    screen.next_card(1)
    assert screen.lbl_card.text == "This feeling is temporary."
    screen.next_card(1)
    assert screen.lbl_card.text == "I am resilient"


def test_cbt_values(data_file, mock_popup):
    screen = CBTValuesScreen()
    screen.in_val.text = "Honesty"
    screen.in_act.text = "Tell the truth today"
    screen.save_val()
    data = load_data()
    assert data["values"][-1]["value"] == "Honesty"


def test_dbt_diary_card(data_file, mock_popup):
    screen = DBTDiaryScreen()
    # FIX: Use the explicit checkboxes dict instead of grid.children
    screen.checkboxes["Describe"].active = True
    screen.checkboxes["Observe"].active = True
    screen.save_diary()
    data = load_data()
    assert len(data["diary_cards"]) == 1
    assert "Describe" in data["diary_cards"][0]["skills"]
    assert "Observe" in data["diary_cards"][0]["skills"]


def test_dbt_dear_man(mock_popup):
    screen = DBTDEARMANScreen()
    screen.in_d.text = "D"
    screen.in_e.text = "E"
    screen.in_a.text = "A"
    screen.in_r.text = "R"
    screen.in_m.text = "M"
    screen.in_a2.text = "A2"
    screen.in_n.text = "N"
    screen.gen_script()
    # FIX: show_popup is mocked, so just verify it was called
    mock_popup.assert_called_once()


def test_dbt_opposite_action(data_file, mock_popup):
    screen = DBTOppositeScreen()
    screen.in_emo.text = "Anger"
    screen.in_opp.text = "Speak softly"
    screen.save_opp()
    data = load_data()
    assert data["opposite_actions"][-1]["emo"] == "Anger"


def test_soothe_senses(data_file, mock_popup):
    screen = SootheSensesScreen()
    screen.in_v.text = "Trees"
    screen.in_h.text = "Birds"
    screen.in_s.text = "Rain"
    screen.in_t.text = "Tea"
    screen.in_o.text = "Blanket"
    screen.save_senses()
    data = load_data()
    assert data["senses"][-1]["v"] == "Trees"
    assert data["senses"][-1]["t"] == "Tea"


def test_tools_mood_tracker(data_file, mock_popup):
    screen = ToolsMoodScreen()
    screen.slider.value = 9
    screen.log_mood()
    data = load_data()
    assert len(data["moods"]) == 1
    assert data["moods"][-1]["mood"] == 9


def test_tools_gratitude(data_file, mock_popup):
    screen = ToolsGratitudeScreen()
    screen.in_g1.text = "Sun"
    screen.in_g2.text = "Tea"
    screen.in_g3.text = "Friends"
    screen.save_grat()
    data = load_data()
    assert "Sun" in data["gratitude"][-1]["items"]


def test_tools_habits(data_file, mock_popup):
    screen = ToolsHabitsScreen()
    screen.cb_sleep.active = True
    screen.cb_meds.active = False
    screen.cb_eat.active = True
    screen.cb_move.active = False
    screen.save_habits()
    data = load_data()
    assert data["habits"]["sleep"] is True
    assert data["habits"]["meds"] is False
    assert data["habits"]["eat"] is True


def test_tools_safety_plan(data_file, mock_popup):
    screen = ToolsSafetyScreen()
    screen.in_warn.text = "Racing thoughts"
    screen.in_cope.text = "Deep breathing"
    screen.in_safe.text = "Call friend"
    screen.save_plan()
    data = load_data()
    assert data["safety_plan"]["warning"] == "Racing thoughts"
    assert data["safety_plan"]["cope"] == "Deep breathing"
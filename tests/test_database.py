from anizoro.database import Database

def test_watchlist_add_list_remove(tmp_path):
    db = Database(tmp_path / "test.db")
    db.add("1535", "Death Note", "https://anilist.co/anime/1535")
    rows = db.list_watchlist()
    assert len(rows) == 1
    assert rows[0]["title"] == "Death Note"
    assert db.remove("1535") is True
    assert db.list_watchlist() == []

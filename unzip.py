
import csv
import chess.pgn
import zstandard as zstd
import io

input_file = "lichess_games.pgn.zst"
output_file = "lichess_games.csv"

# Pour ton extrait, les en-têtes sont ceux de cette liste.
# Pour un fichier complet, découvre-les automatiquement
# comme dans le script du message précédent.
columns = [
    "Event", "Site", "White", "Black", "Result",
    "UTCDate", "UTCTime", "WhiteElo", "BlackElo",
    "WhiteRatingDiff", "BlackRatingDiff", "ECO",
    "Opening", "TimeControl", "Termination", "Moves", "Round", "Date"
]

with open(input_file, "rb") as compressed, \
     open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:

    reader = zstd.ZstdDecompressor().stream_reader(compressed)
    pgn = io.TextIOWrapper(reader, encoding="utf-8", errors="replace")
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    count = 0
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        row = dict(game.headers)
        row["Moves"] = game.accept(
            chess.pgn.StringExporter(
                headers=False, variations=False, comments=False
            )
        )
        writer.writerow(row)
        count += 1

    pgn.close()
    print(f"{count} parties exportées dans {output_file}")

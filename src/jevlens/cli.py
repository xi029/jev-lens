import argparse
import asyncio
import json
from pathlib import Path

import uvicorn

from .config import Settings
from .engine import run_query
from .models import Query
from .samples import DOCUMENTS
from .store import Store


def main():
    parser = argparse.ArgumentParser(description="JevLens — decide before you generate")
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("serve", help="Open the local evidence workbench")
    serve.add_argument("--port", type=int, default=8787)
    sub.add_parser("demo", help="Load the sample documents")
    ask = sub.add_parser("ask", help="Ask a question and print a JSON trace")
    ask.add_argument("question")
    ask.add_argument("--provider", choices=["demo", "ollama", "laya", "jev"])
    ask.add_argument("--generate", action="store_true", help="Use Ollama for accepted answers")
    ingest = sub.add_parser("ingest", help="Import a UTF-8 Markdown or text file")
    ingest.add_argument("path", type=Path)
    args = parser.parse_args()
    settings = Settings()
    if args.command in {None, "serve"}:
        uvicorn.run(
            "jevlens.app:create_app",
            factory=True,
            host="127.0.0.1",
            port=getattr(args, "port", 8787),
        )
        return
    store = Store(settings.data_dir)
    if args.command == "demo":
        for name, text in DOCUMENTS.items():
            store.add_document(name, text)
        print("Sample documents loaded. Run: jevlens serve")
    elif args.command == "ingest":
        if args.path.suffix.lower() not in {".txt", ".md"} or args.path.stat().st_size > 200_000:
            parser.error("Use a UTF-8 .md or .txt file of at most 200 KB.")
        print(
            json.dumps(
                store.add_document(args.path.name, args.path.read_text(encoding="utf-8-sig"))
            )
        )
    elif args.command == "ask":
        trace = asyncio.run(
            run_query(
                store,
                settings,
                Query(
                    question=args.question,
                    provider=args.provider,
                    generator="ollama" if args.generate else "extractive",
                ),
            )
        )
        print(json.dumps(trace, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

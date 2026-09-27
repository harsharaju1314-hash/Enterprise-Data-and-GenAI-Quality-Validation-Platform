"""
Interactive RAG Assistant CLI
"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from rag_engine import EnterpriseRAGEngine

def main():
    print("=" * 65)
    print("Enterprise RAG Knowledge Assistant CLI")
    print("Type a policy question or 'exit' to quit.")
    print("=" * 65)
    
    engine = EnterpriseRAGEngine()
    print(f"[OK] Loaded {len(engine.chunks)} indexed chunks from approved policy documents.\n")
    
    while True:
        try:
            query = input("Ask Query > ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit"):
                break
                
            res = engine.answer_query(query)
            print("-" * 65)
            print(f"Status:   {res['status']}")
            print(f"Source:   {res['source_document']}")
            print(f"Answer:   {res['answer']}")
            if res.get("evidence"):
                print(f"Evidence: {res['evidence']}")
            print("-" * 65 + "\n")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

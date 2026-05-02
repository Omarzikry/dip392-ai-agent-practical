"use client";

import { useState, useRef, useEffect, FormEvent } from "react";

interface AgentResponse {
  query: string;
  is_valid: boolean;
  topics_found: string[];
  answer: string;
  next_steps: string[];
  error: string | null;
}

interface Message {
  id: number;
  role: "user" | "assistant";
  text: string;
  data?: AgentResponse;
}

const SUGGESTIONS = [
  "Explain software testing",
  "What is AI?",
  "Tell me about Python",
  "Show me statistics",
  "How does deployment work?",
  "What are agents?",
];

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const nextId = useRef(1);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function submit(query: string) {
    if (!query.trim() || loading) return;

    const userMsg: Message = { id: nextId.current++, role: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data: AgentResponse = await res.json();

      const assistantMsg: Message = {
        id: nextId.current++,
        role: "assistant",
        text: data.answer || data.error || "No response.",
        data,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      setMessages((prev) => [
        ...prev,
        {
          id: nextId.current++,
          role: "assistant",
          text: `Could not reach the study agent. Make sure the Python server is running on port 8000.\n\n${msg}`,
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    submit(input);
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className="flex-none border-b border-gray-800 px-6 py-4 flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">
          S
        </div>
        <div>
          <h1 className="font-semibold text-white text-sm">Study Assistant</h1>
          <p className="text-xs text-gray-500">Powered by your local knowledge base</p>
        </div>
        <span className="ml-auto flex items-center gap-1.5 text-xs text-emerald-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
          API on :8000
        </span>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center gap-6">
            <div className="w-16 h-16 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center">
              <span className="text-3xl">📚</span>
            </div>
            <div>
              <h2 className="text-xl font-semibold text-white mb-1">What do you want to study?</h2>
              <p className="text-sm text-gray-500 max-w-sm">
                Ask about software testing, AI, Python, statistics, deployment, or agents.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-2 w-full max-w-md">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => submit(s)}
                  className="text-left text-sm px-3 py-2 rounded-lg border border-gray-700 text-gray-300 hover:border-indigo-500 hover:text-white hover:bg-indigo-600/10 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "assistant" && (
              <div className="flex-none w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-xs font-bold mt-0.5">
                S
              </div>
            )}

            <div className={`max-w-2xl ${msg.role === "user" ? "items-end" : "items-start"} flex flex-col gap-2`}>
              {msg.role === "user" ? (
                <div className="bg-indigo-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-sm text-sm">
                  {msg.text}
                </div>
              ) : (
                <div className="flex flex-col gap-3 w-full">
                  {/* Main answer */}
                  <div className="bg-gray-800/60 border border-gray-700/50 rounded-2xl rounded-tl-sm px-4 py-3">
                    {msg.data?.error ? (
                      <p className="text-red-400 text-sm">{msg.data.error}</p>
                    ) : (
                      <pre className="text-sm text-gray-200 whitespace-pre-wrap font-sans leading-relaxed">
                        {msg.text}
                      </pre>
                    )}
                  </div>

                  {/* Topics */}
                  {msg.data && msg.data.topics_found.length > 0 && (
                    <div className="flex flex-wrap gap-1.5">
                      {msg.data.topics_found.map((t) => (
                        <span
                          key={t}
                          className="text-xs px-2.5 py-1 rounded-full bg-indigo-600/20 border border-indigo-500/30 text-indigo-300"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Next steps */}
                  {msg.data && msg.data.next_steps.length > 0 && (
                    <div className="bg-gray-800/40 border border-gray-700/40 rounded-xl px-4 py-3">
                      <p className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-2">
                        Recommended next steps
                      </p>
                      <ul className="space-y-1.5">
                        {msg.data.next_steps.map((step, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                            <span className="flex-none mt-0.5 w-4 h-4 rounded-full bg-indigo-600/30 text-indigo-400 text-xs flex items-center justify-center font-medium">
                              {i + 1}
                            </span>
                            {step}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>

            {msg.role === "user" && (
              <div className="flex-none w-7 h-7 rounded-lg bg-gray-700 flex items-center justify-center text-gray-300 text-xs font-bold mt-0.5">
                U
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 justify-start">
            <div className="flex-none w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-xs font-bold">
              S
            </div>
            <div className="bg-gray-800/60 border border-gray-700/50 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1 items-center h-4">
                <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:0ms]" />
                <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:150ms]" />
                <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="flex-none border-t border-gray-800 px-4 py-4">
        <form onSubmit={handleSubmit} className="flex gap-2 max-w-3xl mx-auto">
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a study question..."
            disabled={loading}
            className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 disabled:opacity-50 transition-colors"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex-none bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl px-4 py-3 text-sm font-medium transition-colors"
          >
            Send
          </button>
        </form>
        <p className="text-center text-xs text-gray-600 mt-2">
          Topics: testing · deployment · AI · agents · Python · statistics
        </p>
      </div>
    </div>
  );
}

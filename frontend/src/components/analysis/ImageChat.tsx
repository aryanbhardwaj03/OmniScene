"use client";

import { useState, useRef, useEffect } from 'react';
import { sendChatMessage, ChatMessage } from '@/lib/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Props {
  analysisId: string;
}

export default function ImageChat({ analysisId }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage, { role: 'assistant', content: '' }]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Send the current history (excluding the new user and empty assistant messages)
      const currentHistory = messages.filter(m => m.content); 
      await sendChatMessage(analysisId, userMessage.content, currentHistory, (chunk) => {
        setMessages(prev => {
          const newMessages = [...prev];
          const lastIndex = newMessages.length - 1;
          newMessages[lastIndex] = {
            ...newMessages[lastIndex],
            content: newMessages[lastIndex].content + chunk
          };
          return newMessages;
        });
      });
    } catch (err: any) {
      console.error("Chat error:", err);
      setError("Failed to send message. Please ensure the Groq API key is configured.");
      // Remove the user and empty assistant message if it failed completely
      setMessages(prev => prev.slice(0, -2));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-card flex flex-col h-[500px] overflow-hidden border border-white/10 relative">
      <div className="p-4 border-b border-white/10 bg-secondary/20">
        <h3 className="font-semibold flex items-center gap-2">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
          Ask AI About This Image
        </h3>
        <p className="text-xs text-muted-foreground mt-1">Powered by Groq Vision API</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground mt-10 text-sm">
            <div className="bg-secondary/30 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            </div>
            <p>Ask anything about the subject in the photo!</p>
            <p className="text-xs mt-2 opacity-70">e.g., "Is this plant safe for cats?" or "What breed mix could this dog be?"</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div 
              className={`max-w-[85%] rounded-2xl p-3 text-sm ${
                msg.role === 'user' 
                  ? 'bg-primary text-primary-foreground rounded-tr-sm' 
                  : 'bg-secondary/50 border border-white/5 rounded-tl-sm prose prose-sm prose-invert max-w-none'
              }`}
            >
              {msg.role === 'assistant' ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        
        {isLoading && !messages[messages.length - 1]?.content && (
          <div className="flex justify-start">
            <div className="bg-secondary/50 border border-white/5 rounded-2xl rounded-tl-sm p-4 flex items-center gap-2">
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="p-3 mx-4 mb-2 bg-destructive/20 border border-destructive/50 text-destructive text-xs rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="p-4 bg-background/50 border-t border-white/10 backdrop-blur-md">
        <div className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={isLoading}
            className="premium-input w-full pr-14"
          />
          <button 
            type="submit" 
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 bg-primary text-primary-foreground rounded-xl disabled:opacity-50 hover:bg-primary/90 transition-all shadow-md hover:shadow-primary/20 hover:scale-105 active:scale-95 flex items-center justify-center"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
      </form>
    </div>
  );
}

"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
      const res = await fetch(`${API_BASE}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to sign up');
      }
      
      router.push('/login');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-4">
      <div className="glass-card w-full max-w-md p-8 rounded-2xl">
        <h1 className="text-2xl font-bold text-center mb-6">Create an Account</h1>
        {error && <div className="text-destructive bg-destructive/10 p-3 rounded mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSignup} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input 
              type="email" 
              required 
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-background/50 border border-border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" 
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input 
              type="password" 
              required 
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-background/50 border border-border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" 
            />
          </div>
          <button type="submit" className="w-full py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition">
            Sign Up
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-muted-foreground">
          Already have an account? <a href="/login" className="text-primary hover:underline">Login</a>
        </p>
      </div>
    </div>
  );
}

"use client";

import Link from 'next/link';
import { useAuthStore } from '@/lib/store';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center px-4 mx-auto justify-between">
        <div className="flex md:flex">
          <Link href="/" className="flex items-center space-x-2">
            <span className="font-bold sm:inline-block text-xl">
              Omni<span className="text-primary">Scene</span>
            </span>
          </Link>
          <nav className="flex items-center gap-6 text-sm ml-6">
            <Link href="/analyze" className="transition-colors hover:text-foreground/80 text-foreground/60">
              Analyze
            </Link>
            <Link href="/history" className="transition-colors hover:text-foreground/80 text-foreground/60">
              History
            </Link>
          </nav>
        </div>
        
        <div className="flex items-center gap-4 text-sm">
          {user ? (
            <>
              <span className="text-muted-foreground">{user.email}</span>
              <button onClick={handleLogout} className="text-primary hover:underline">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-foreground/60 hover:text-foreground">
                Login
              </Link>
              <Link href="/signup" className="bg-primary text-primary-foreground px-4 py-1.5 rounded-full font-medium hover:bg-primary/90 transition-colors">
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

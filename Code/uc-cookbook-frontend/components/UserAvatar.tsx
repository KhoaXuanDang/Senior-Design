'use client';

import { cn } from '@/lib/utils';

function initials(username: string): string {
  const parts = username.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return username.slice(0, 2).toUpperCase() || '?';
}

function hueFromString(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h + s.charCodeAt(i) * 17) % 360;
  return h;
}

type Size = 'sm' | 'md' | 'lg';

const sizeClass: Record<Size, string> = {
  sm: 'h-8 w-8 text-xs',
  md: 'h-10 w-10 text-sm',
  lg: 'h-12 w-12 text-base',
};

export function UserAvatar({
  username,
  className,
  size = 'md',
}: {
  username: string;
  className?: string;
  size?: Size;
}) {
  const h = hueFromString(username);
  return (
    <div
      className={cn(
        'flex shrink-0 items-center justify-center rounded-full font-semibold text-white ring-2 ring-background',
        sizeClass[size],
        className
      )}
      style={{ backgroundColor: `hsl(${h} 55% 42%)` }}
      aria-hidden
    >
      {initials(username)}
    </div>
  );
}

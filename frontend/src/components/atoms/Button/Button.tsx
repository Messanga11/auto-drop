'use client';

import React from 'react';
import { cn } from '@/lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'tag';
  size?: 'sm' | 'md' | 'lg';
  state?: 'active' | 'inactive';
  children: React.ReactNode;
}

export function Button({
  variant = 'default',
  size = 'md',
  state,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  if (variant === 'tag') {
    const isActive = state === 'active';
    return (
      <button
        className={cn(
          'btn-tag font-regular',
          isActive ? 'btn-tag-active' : 'btn-tag-inactive',
          'text-text-primary',
          disabled && 'opacity-50 cursor-not-allowed',
          className
        )}
        disabled={disabled}
        {...props}
      >
        {children}
      </button>
    );
  }

  // Default variant
  return (
    <button
      className={cn(
        'btn-default font-regular',
        'text-text-primary',
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}

'use client';

import React, { useId } from 'react';
import { cn } from '@/lib/utils';

export interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  error?: string;
}

export function Switch({
  label,
  error,
  className,
  id,
  ...props
}: SwitchProps) {
  const generatedId = useId();
  const switchId = id || generatedId;

  return (
    <div className={cn('flex items-center gap-component', className)}>
      <div className="relative inline-flex items-center">
        <input
          type="checkbox"
          id={switchId}
          role="switch"
          className={cn(
            'sr-only',
            className
          )}
          {...props}
        />
        <label
          htmlFor={switchId}
          className={cn(
            'relative',
            'inline-block',
            'w-11',
            'h-6',
            'rounded-full',
            'cursor-pointer',
            'transition-colors duration-200',
            'bg-background-glass',
            'border-2',
            'border-background-glass',
            props.checked && 'bg-primary',
            props.checked && 'border-primary',
            'focus-within:ring-2',
            'focus-within:ring-primary',
            'focus-within:ring-offset-2',
            'focus-within:ring-offset-background-dark',
            props.disabled && 'opacity-50',
            props.disabled && 'cursor-not-allowed',
            error && 'border-accent-red',
            error && 'focus-within:ring-accent-red'
          )}
        >
          <span
            className={cn(
              'absolute',
              'top-0.5',
              'left-0.5',
              'w-5',
              'h-5',
              'rounded-full',
              'bg-white',
              'transition-transform duration-200',
              'transform',
              props.checked ? 'translate-x-5' : 'translate-x-0'
            )}
          />
        </label>
      </div>
      {label && (
        <label
          htmlFor={switchId}
          className={cn(
            'text-body-regular',
            'font-regular',
            'text-text-primary',
            'cursor-pointer',
            'select-none',
            error && 'text-accent-red'
          )}
        >
          {label}
        </label>
      )}
      {error && (
        <span className="text-body-small text-accent-red mt-1">
          {error}
        </span>
      )}
    </div>
  );
}


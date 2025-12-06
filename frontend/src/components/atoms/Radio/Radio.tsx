'use client';

import React, { useId } from 'react';
import { cn } from '@/lib/utils';

export interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  error?: string;
}

export function Radio({
  label,
  error,
  className,
  id,
  name,
  ...props
}: RadioProps) {
  const generatedId = useId();
  const radioId = id || generatedId;

  return (
    <div className={cn('flex items-center gap-component', className)}>
      <div className="relative flex items-center">
        <input
          type="radio"
          id={radioId}
          name={name}
          className={cn(
            'appearance-none',
            'w-5 h-5',
            'rounded-full',
            'border-2',
            'border-background-glass',
            'bg-background-card',
            'cursor-pointer',
            'transition-all duration-200',
            'checked:bg-primary',
            'checked:border-primary',
            'checked:after:content-[""]',
            'checked:after:w-2',
            'checked:after:h-2',
            'checked:after:rounded-full',
            'checked:after:bg-white',
            'checked:after:absolute',
            'checked:after:top-1/2',
            'checked:after:left-1/2',
            'checked:after:-translate-x-1/2',
            'checked:after:-translate-y-1/2',
            'focus:outline-none',
            'focus:ring-2',
            'focus:ring-primary',
            'focus:ring-offset-2',
            'focus:ring-offset-background-dark',
            'disabled:opacity-50',
            'disabled:cursor-not-allowed',
            error && 'border-accent-red',
            className
          )}
          {...props}
        />
      </div>
      {label && (
        <label
          htmlFor={radioId}
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


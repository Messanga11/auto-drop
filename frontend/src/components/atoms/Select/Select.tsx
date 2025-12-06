'use client';

import React, { useId } from 'react';
import { cn } from '@/lib/utils';
import { ChevronDown } from 'lucide-react';

export interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
}

export interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'children'> {
  options: SelectOption[];
  placeholder?: string;
  error?: string;
  label?: string;
}

export function Select({
  options,
  placeholder,
  error,
  label,
  className,
  id,
  ...props
}: SelectProps) {
  const generatedId = useId();
  const selectId = id || generatedId;

  return (
    <div className={cn('flex flex-col gap-component', className)}>
      {label && (
        <label
          htmlFor={selectId}
          className={cn(
            'text-body-regular',
            'font-regular',
            'text-text-primary',
            error && 'text-accent-red'
          )}
        >
          {label}
        </label>
      )}
      <div className="relative">
        <select
          id={selectId}
          className={cn(
            'appearance-none',
            'w-full',
            'px-component',
            'py-3',
            'rounded-md',
            'bg-background-card',
            'border-2',
            'border-background-glass',
            'text-text-primary',
            'text-body-regular',
            'font-regular',
            'cursor-pointer',
            'transition-all duration-200',
            'focus:outline-none',
            'focus:ring-2',
            'focus:ring-primary',
            'focus:border-primary',
            'focus:ring-offset-2',
            'focus:ring-offset-background-dark',
            'disabled:opacity-50',
            'disabled:cursor-not-allowed',
            'pr-10',
            error && 'border-accent-red',
            error && 'focus:ring-accent-red',
            className
          )}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option
              key={option.value}
              value={option.value}
              disabled={option.disabled}
              className="bg-background-dark text-text-primary"
            >
              {option.label}
            </option>
          ))}
        </select>
        <ChevronDown
          className={cn(
            'absolute',
            'right-component',
            'top-1/2',
            '-translate-y-1/2',
            'w-5 h-5',
            'text-text-secondary',
            'pointer-events-none',
            'transition-transform duration-200',
            'peer-focus:rotate-180'
          )}
        />
      </div>
      {error && (
        <span className="text-body-small text-accent-red">
          {error}
        </span>
      )}
    </div>
  );
}


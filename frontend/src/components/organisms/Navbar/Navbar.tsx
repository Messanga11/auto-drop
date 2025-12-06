'use client';

import React from 'react';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Icon } from '@/components/atoms/Icon/Icon';
import { cn } from '@/lib/utils';
import { Menu, Bell, User, LucideIcon } from 'lucide-react';

export interface NavbarProps {
  user?: {
    name: string;
    avatar?: string;
  };
  onLogout?: () => void;
  items?: Array<{
    label: string;
    href: string;
    icon?: LucideIcon;
  }>;
  className?: string;
}

export function Navbar({
  user,
  onLogout,
  items = [],
  className,
}: NavbarProps) {
  const pathname = usePathname();

  return (
    <nav
      className={cn(
        'fixed top-0 left-0 right-0 z-50',
        'flex items-center justify-between',
        'navbar-height',
        'px-screen',
        'backdrop-blur-card',
        'bg-[rgba(0,0,0,0.30)]',
        className
      )}
    >
      <div className="flex items-center gap-section">
        {items.map((item, index) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          return (
            <a
              key={index}
              href={item.href}
              className={cn(
                'flex items-center gap-component',
                'transition-colors duration-200',
                'relative',
                isActive
                  ? 'text-primary'
                  : 'text-text-primary hover:text-primary'
              )}
            >
              {item.icon && <Icon icon={item.icon as any} size={20} />}
              <span className="text-body-regular font-regular">{item.label}</span>
              {isActive && (
                <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-full" />
              )}
            </a>
          );
        })}
      </div>

      <div className="flex items-center gap-component">
        <Icon icon={Bell} size={20} />
        {user && (
          <div className="flex items-center gap-component">
            {user.avatar ? (
              <Image
                src={user.avatar}
                alt={user.name}
                width={42}
                height={42}
                className="navbar-avatar rounded-full"
              />
            ) : (
              <div className="navbar-avatar rounded-full bg-primary flex items-center justify-center">
                <Icon icon={User} size={20} />
              </div>
            )}
            {onLogout && (
              <button
                onClick={onLogout}
                className="text-body-regular text-text-secondary hover:text-text-primary transition-colors"
              >
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

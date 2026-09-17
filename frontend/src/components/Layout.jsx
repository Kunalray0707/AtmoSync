import { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const navItems = [
	{ to: '/dashboard', label: 'Dashboard' },
	{ to: '/commodities', label: 'Commodities' },
	{ to: '/sensors', label: 'Sensors' },
	{ to: '/alerts', label: 'Alerts' },
	{ to: '/upload', label: 'Upload data' },
	{ to: '/profile', label: 'Profile' },
];

export default function Layout() {
	const { user, logout } = useAuth();
	const navigate = useNavigate();

	const signOut = () => {
		logout();
		navigate('/login');
	};

	return (
		<div className="min-h-screen bg-gray-50">
			<header className="border-b border-gray-200 bg-white">
				<div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
					<NavLink to="/dashboard" className="text-xl font-bold text-primary-700">AtmoSync</NavLink>
					<div className="flex items-center gap-4 text-sm">
						<span className="text-gray-600">{user?.full_name || user?.username}</span>
						<button type="button" onClick={signOut} className="btn-secondary">Sign out</button>
					</div>
				</div>
			</header>
			<div className="mx-auto flex max-w-7xl gap-6 px-4 py-6">
				<nav className="hidden w-52 shrink-0 space-y-1 md:block">
					{navItems.map((item) => (
						<NavLink key={item.to} to={item.to} className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
							{item.label}
						</NavLink>
					))}
				</nav>
				<main className="min-w-0 flex-1"><Outlet /></main>
			</div>
		</div>
	);
}

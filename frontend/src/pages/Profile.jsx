import { useAuth } from '../hooks/useAuth';

export default function Profile() {
  const { user } = useAuth();
  return <section><h1 className="card-header">Profile</h1><div className="card space-y-3"><p><strong>Username:</strong> {user?.username}</p><p><strong>Email:</strong> {user?.email}</p><p><strong>Role:</strong> {user?.role}</p></div></section>;
}
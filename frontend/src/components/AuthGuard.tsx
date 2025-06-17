import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface AuthGuardProps {
  children: React.ReactNode;
}

const AuthGuard: React.FC<AuthGuardProps> = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token'); // Assuming token is stored in localStorage
    if (!token) {
      navigate('/login', { replace: true });
    }
  }, [navigate]);

  return <>{children}</>;
};

export default AuthGuard;
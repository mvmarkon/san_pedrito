import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';
import api from '@/lib/api';
import { z } from 'zod';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const registerSchema = z
  .object({
    email: z.string().email({ message: 'Ingrese un email válido' }),
    password: z
      .string()
      .min(6, { message: 'La contraseña debe tener al menos 6 caracteres' }),
    confirmPassword: z.string(),
    first_name: z.string().min(1, { message: 'El nombre es requerido' }),
    last_name: z.string().min(1, { message: 'El apellido es requerido' }),
    document_number: z.string().min(1, { message: 'El número de documento es requerido' }),
    phone_number: z.string().optional(),
    address: z.string().optional(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Las contraseñas no coinciden',
    path: ['confirmPassword'],
  });

type RegisterFormValues = z.infer<typeof registerSchema>;

interface RegisterFormProps {
  onSuccess?: () => void;
}

const RegisterForm = ({ onSuccess }: RegisterFormProps) => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
      first_name: '',
      last_name: '',
      document_number: '',
      phone_number: '',
      address: '',
    },
  });

  const onSubmit = async (data: RegisterFormValues) => {
    setIsLoading(true);

    try {
      const response = await api.post('/clientes/', {
        email: data.email,
        password: data.password,
        nombre: data.first_name,
        apellido: data.last_name,
        document_number: data.document_number,
        phone_number: data.phone_number,
        address: data.address,
      });

      toast({
        title: 'Registro exitoso',
        description: 'Su cuenta ha sido creada. Ahora puede iniciar sesión.',
      });

      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      console.error('Error de registro:', error);
      let errorMessage = 'Error al registrar el usuario. Intente nuevamente.';
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      toast({
        variant: 'destructive',
        title: 'Error de registro',
        description: errorMessage,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="grid gap-4">
      <div className="grid gap-2">
        <Label htmlFor="register-first_name">Nombre</Label>
        <Input
          id="register-first_name"
          placeholder="Su nombre"
          type="text"
          autoCapitalize="words"
          disabled={isLoading}
          {...register('first_name')}
        />
        {errors.first_name && (
          <p className="text-sm text-destructive">
            {errors.first_name.message}
          </p>
        )}
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-last_name">Apellido</Label>
        <Input
          id="register-last_name"
          placeholder="Su apellido"
          type="text"
          autoCapitalize="words"
          disabled={isLoading}
          {...register('last_name')}
        />
        {errors.last_name && (
          <p className="text-sm text-destructive">
            {errors.last_name.message}
          </p>
        )}
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-email">Email</Label>
        <Input
          id="register-email"
          placeholder="nombre@ejemplo.com"
          type="email"
          autoCapitalize="none"
          autoComplete="email"
          autoCorrect="off"
          disabled={isLoading}
          {...register('email')}
        />
        {errors.email && (
          <p className="text-sm text-destructive">{errors.email.message}</p>
        )}
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-password">Contraseña</Label>
        <Input
          id="register-password"
          type="password"
          autoCapitalize="none"
          autoComplete="new-password"
          disabled={isLoading}
          {...register('password')}
        />
        {errors.password && (
          <p className="text-sm text-destructive">
            {errors.password.message}
          </p>
        )}
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-confirmPassword">Confirmar Contraseña</Label>
        <Input
          id="register-confirmPassword"
          type="password"
          autoCapitalize="none"
          autoComplete="new-password"
          disabled={isLoading}
          {...register('confirmPassword')}
        />
        {errors.confirmPassword && (
          <p className="text-sm text-destructive">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-phone_number">Teléfono (Opcional)</Label>
        <Input
          id="register-phone_number"
          placeholder="123-456-7890"
          type="tel"
          disabled={isLoading}
          {...register('phone_number')}
        />
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-address">Dirección (Opcional)</Label>
        <Input
          id="register-address"
          placeholder="Calle, número, ciudad"
          type="text"
          disabled={isLoading}
          {...register('address')}
        />
      </div>
      <div className="grid gap-2">
        <Label htmlFor="register-document_number">Número de Documento</Label>
        <Input
          id="register-document_number"
          placeholder="Su número de documento"
          type="text"
          disabled={isLoading}
          {...register('document_number')}
        />
        {errors.document_number && (
          <p className="text-sm text-destructive">
            {errors.document_number.message}
          </p>
        )}
      </div>
      <Button type="submit" disabled={isLoading}>
        {isLoading ? 'Registrando...' : 'Registrarse'}
      </Button>
    </form>
  );
};

export default RegisterForm;
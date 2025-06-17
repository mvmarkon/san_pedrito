import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 text-center">
      <h1 className="text-6xl font-bold">404</h1>
      <h2 className="mt-4 text-2xl font-semibold">Página no encontrada</h2>
      <p className="mt-2 text-muted-foreground">
        Lo sentimos, la página que estás buscando no existe o ha sido movida.
      </p>
      <Button asChild className="mt-8">
        <Link to="/">Volver al inicio</Link>
      </Button>
    </div>
  )
}

export default NotFound
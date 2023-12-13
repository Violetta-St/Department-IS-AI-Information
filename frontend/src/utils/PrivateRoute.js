import { Route, useNavigate } from 'react-router-dom'
import { useContext, useEffect  } from 'react'
import AuthContext from '../context/AuthContext'

const PrivateRoute = ({children}) => {
    let {user} = useContext(AuthContext)
    const navigate = useNavigate();
    useEffect(() => {
    if (!user) {
        navigate("/login");
    }
    }, []);

    return user?<>{children}</>:<></>

}

export default PrivateRoute;
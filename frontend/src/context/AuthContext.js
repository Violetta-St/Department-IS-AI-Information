import { createContext } from 'react'



const AuthContext = createContext({
    user:'',
    authTokens:'',
    loginUser:'',
    logoutUser:'',
})

export default AuthContext;
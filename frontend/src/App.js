import './App.css';
import AuthProvider from './context/AuthContext'
import { useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";

import { BrowserRouter, Route, Routes } from 'react-router-dom'
import PrivateRoute from './utils/PrivateRoute'

import Header from './components/Header'
import HomePage from './components/homepage/HomePage'
import LoginPage from './components/login/LoginPage'
import StudentPage from './components/student/StudentPage'
import EducatorPage from './components/educator/EducatorPage'
import CreateEducator from './components/admin/AdminPage'
import ForumPage from './components/forum/ForumPage'


function App() {
  let [authTokens, setAuthTokens] = useState(()=> localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
  let [user, setUser] = useState(()=> localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null)

  let loginUser = async (e)=> {
      e.preventDefault()
       fetch('http://localhost:8000/api/token/', {
          method:'POST',
          headers:{
              'Content-Type':'application/json'
          },
          body:JSON.stringify({'username':e.target.username.value, 'password':e.target.password.value})
      }).then((response) => {
        if(response.status === 200){
          response.json().then((data) => {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
            window.location.pathname = '/'
          })
      }else{
          alert('Something went wrong!')
      }
      }).catch((error) => console.log(error))
  }


  let logoutUser = () => {
      setAuthTokens(null)
      setUser(null)
      localStorage.removeItem('authTokens')
      window.location.pathname = '/login'
  }


  let updateToken = async ()=> {

      fetch(`${process.env.REACT_APP_API_KEY}refresh/`, {
          method:'POST',
          headers:{
              'Content-Type':'application/json'
          },
          body:JSON.stringify({'refresh':authTokens?.refresh})
      }).then((response) => {
        if (response.status === 200){
          response.json().then((data) => {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
          })
      }else{
          logoutUser()
      }

      }).catch((err) => console.log(err))
  }

  useEffect(()=> {
    if (!authTokens) {

        let fourMinutes = 1000 * 60 * 4

        let interval =  setInterval(()=> {
            if(authTokens){
                updateToken()
            }
        }, fourMinutes)
        return ()=> clearInterval(interval)
    }
  }, [authTokens, updateToken])
  let contextData = {
    user:user,
    authTokens:authTokens,
    loginUser:loginUser,
    logoutUser:logoutUser,
}
  return (
    <div className="App">

    <AuthProvider.Provider value={contextData}>
       <BrowserRouter>
       <Header/>
             <Routes>
                 <Route element={<PrivateRoute><HomePage /></PrivateRoute>}path="/home"exact/>
                 <Route element={<PrivateRoute><StudentPage /></PrivateRoute>} path="/student" exact/>
                 <Route element={<PrivateRoute><EducatorPage /></PrivateRoute>} path="/educator" exact/>
                 <Route element={<PrivateRoute><ForumPage /></PrivateRoute>} path="/forum" exact/>
                 <Route element={<PrivateRoute><CreateEducator /></PrivateRoute>} path="/admin" exact/>
                 <Route element={<LoginPage />} path="/login"/>
             </Routes>
        </BrowserRouter>
    </AuthProvider.Provider>

    </div>
  );
}

export default App;
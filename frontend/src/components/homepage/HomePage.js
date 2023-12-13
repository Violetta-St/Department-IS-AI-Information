import React, {useContext} from 'react'
import AuthContext from '../../context/AuthContext'
import { Link } from 'react-router-dom';

const HomePage = () => {
    return (
        <div>
            <Link to="/student">Студенты</Link>
            <Link to="/educator">Преподаватели</Link>
            <Link to="/forum">Форум</Link>
        </div>
    )
}

export default HomePage
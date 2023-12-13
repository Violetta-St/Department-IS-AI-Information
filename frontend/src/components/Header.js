import React from "react";
import { Link } from 'react-router-dom';

const Header = () => {
    return <nav>
    <ul>
      <li>
        <Link to="/home">Главная</Link>
      </li>
      <li>
        <Link to="/student">Студенты</Link>
      </li>
      <li>
        <Link to="/educator">Преподаватели</Link>
      </li>
      <li>
        <Link to="/forum">Форум</Link>
      </li>
      <li>
        <Link to="/admin">Администратор</Link>
      </li>
      <li>
        <Link to="/login">Войти</Link>
      </li>

    </ul>
  </nav>
}

export default  Header;
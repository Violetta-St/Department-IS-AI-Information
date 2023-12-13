import React, { useState, useContext } from 'react';
import { Button, Checkbox, Form, Table } from 'semantic-ui-react'
import AuthContext from '../../context/AuthContext'

const API_URL = 'http://localhost:8000/api/admin';

const CreateEducator = () => {
    let {authTokens, logoutUser} = useContext(AuthContext)
    const [educatorData, setEducatorData] = useState({});
    const [checked, setChecked] = useState(true);


    let postData = async(e) =>{
        const body = JSON.stringify({'username':e.target.username.value, 'password':e.target.password.value,
         'firstname': e.target.firstname.value, 'lastname': e.target.lastname.value,
            'phone': e.target.phone.value, 'patronymic': e.target.patronymic.value,
            'email':e.target.email.value, 'academic_degree': e.target.academic_degree.value,
            'department_head': checked})
        console.log(body)
        let response = await fetch(`${API_URL}/new_educator/`, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            },
            body:body
        })
        let data = await response.json()

        if(response.status === 200){
            setEducatorData(data)
        }
        }
    return (
        <div>
            <form onSubmit={postData}>
                <input type="text" name="username" placeholder="логин" />
                <input type="text" name="password" placeholder="пароль"/>
                <input type="text" name="lastname" placeholder="фамилия"/>
                <input type="text" name="firstname" placeholder="имя"/>
                <input type="text" name="patronymic" placeholder="отчество"/>
                <input type="text" name="email" placeholder="email" />
                <input type="text" name="phone" placeholder="номер телефона" />
                <input type="checkbox" checked={checked} onChange={() => setChecked(!checked)} />
                <select name='academic_degree'>
                        <option value="AS">Ассистент</option>
                        <option value="ST">Старший преподаватель</option>
                        <option value="DC">Доцент</option>
                        <option value="PR">Профессор</option>
                    </select>
                <input type="submit"/>
            </form>
        </div>
    )
}


export default CreateEducator



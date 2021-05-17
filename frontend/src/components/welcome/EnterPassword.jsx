import { Component, Fragment } from 'react'

import styles from './Styles'
import Button from '../Button'

import Person from '../../assets/img/person.png'
import Swal from 'sweetalert2'

class EnterPassword extends Component {
    constructor (props) {
        super(props)
        this.state = { password: "", step: 0, checkPassword: "" }    
        this.setPassword = this.setPassword.bind(this)
        this.next = this.next.bind(this)
        this.setCheckPassword = this.setCheckPassword.bind(this)
        this.validate = this.validate.bind(this)
    }
    
    setPassword (event) {
        this.setState({ password: event.target.value })
    }

    next () {
        this.setState({ step: this.state.step + 1 })
    }

    validate () {

        const setPasswordAPI = () => {
            fetch(`${process.env.REACT_APP_BASE_API_URL}/users/registration/step-2`, {
                method: "POST",
                headers: new Headers({
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }),
                body: JSON.stringify({
                    username: this.props.meta.name,
                    email: this.props.meta.email,
                    password: this.state.password
                })
            })
            .then(res => res.json())
            .then(() => {
                Swal.fire({
                    icon: 'success',
                    title: 'Good',
                    text: "Your account has been registered",
                    showConfirmButton: false,
                    timer: 2500
                })
            })
            .catch(() => Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong...'
            }))
        }
        
        if (this.state.password !== this.state.checkPassword) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: "Passwords don't match"
            })
            this.setState({ step: 0, password: "", checkPassword: "" })
        } else {
            setPasswordAPI()
        }
    }

    setCheckPassword (event) {
        this.setState({ checkPassword: event.target.value })
    }

    stepOne() {
        return (
            <Fragment>
                <div style={styles._wrap}>
                    <div className="welcome_1 screen__center text__center" style={styles.component}>
                        <div className="welcome_1__item text-gray-800" style={styles.item}>
                            <img src={Person} alt="wave" style={styles.img} />
                            <p className="op_text">Create the password</p>
                        </div>
                        <div><input type="password" value={this.state.password} style={styles.input} onChange={this.setPassword} /></div>
                        <br />
                        <p className="op_text" style={styles.min_text}>Create password which will be passphrase to enter to your account.</p>
                        <div className="buttons">
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Back" click={this.props.back} />
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Send" click={this.next} />
                        </div>
                    </div>   
                </div>
            </Fragment>
        )
    }

    stepTwo() {
        return (
            <Fragment>
                <div style={styles._wrap}>
                    <div className="welcome_1 screen__center text__center" style={styles.component}>
                        <div className="welcome_1__item text-gray-800" style={styles.item}>
                            <img src={Person} alt="wave" style={styles.img} />
                            <p className="op_text">Check the password</p>
                        </div>
                        <div><input type="password" value={this.state.checkPassword} style={styles.input} onChange={this.setCheckPassword} /></div>
                        <br />
                        <p className="op_text" style={styles.min_text}>Enter the password again.</p>
                        <div className="buttons">
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Back" click={this.props.back} />
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Send" click={this.validate} />
                        </div>
                    </div>   
                </div>
            </Fragment>
        )
    }
 
    render () {
        if (this.state.step === 0) return this.stepOne()
        else if (this.state.step === 1) return this.stepTwo()
    }
}

export default EnterPassword

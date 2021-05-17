import Swal from 'sweetalert2'
import { Component, Fragment } from 'react'


import styles from './Styles'
import Button from '../Button'

import Mobile from '../../assets/img/mobile.png'



class EnterPhone extends Component {
    constructor (props) {
        super(props)
        this.state = { email: "", step: 0, code: "", time: 0 }
        this.back = this.back.bind(this)
        this.setEmail = this.setEmail.bind(this)
        this.goNextStep = this.goNextStep.bind(this)
        this.setConfirmationCode = this.setConfirmationCode.bind(this)
        this.sendConfirmationCodeAPI = this.sendConfirmationCodeAPI.bind(this)
    }

    componentDidMount () {
        setInterval(() => {
            this.setState({ time: this.state.time + 1 })
        }, 1000)
    }

    componentWillUnmount () {
        clearInterval(this.state.time)
    }

    setEmail (event) {
        this.setState({ email: event.target.value })
    }

    back () {
        this.setState({ step: this.state.step - 1 })
    }

    setConfirmationCode (code) {
        this.setState({ code: code.target.value })
    }

    sendConfirmationCodeAPI = () => {
        return fetch(`${process.env.REACT_APP_BASE_API_URL}/users/registration/step-1`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                username: this.props.meta.name,
                email: this.state.email
            })
        })
        .then(res => res.json())
        .then(json => {
            if (Object.keys(json).includes("detail")) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: json.detail
                })
                return false
            }
            return true
        })
    }

    goNextStep () {

        const validateEmail = () => {
            let isValid = true
            const emailno = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            
            if (!emailno.test(this.state.email)) {
                isValid = false
            }

            return isValid
        }


        this.sendConfirmationCodeAPI()
            .then(status => {
                if (status) {
                    if (!validateEmail()) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: "You haven't entered email or email address is incorrect"
                        })
                    } else {
                        this.setState({ step: this.state.step + 1 })
                    }
                }
            })
    }

    stepOne () {
        return (
            <Fragment>
                <div style={styles._wrap}>
                    <div className="welcome_1 screen__center text__center" style={styles.component}>
                        <div className="welcome_1__item text-gray-800" style={styles.item}>
                            <img src={Mobile} alt="wave" style={styles.img} />
                            <p className="op_text">Enter your email account address</p>
                        </div>
                        <div><input type="email" value={this.state.email} style={styles.input} onChange={this.setEmail} /></div>
                        <br />
                        <p className="op_text" style={styles.min_text}>We will send you confirmation code, to your email.</p>
                        <div className="buttons">
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Back" click={this.props.back} />
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Send" click={this.state.step === 0 ? this.goNextStep : this.props.next} />
                        </div>
                    </div>   
                </div>
            </Fragment>
        )
    }

    stepTwo () {
        const verifyConfirmationCodeAPI = () => {
            fetch(`${process.env.REACT_APP_BASE_API_URL}/users/email-confirmation`, {
                method: "POST",
                headers: new Headers({
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }),
                body: JSON.stringify({
                    username: this.props.meta.name,
                    email: this.state.email,
                    token: this.state.code
                })
            })
            .then(res => res.json())
            .then(json => {
                if (!json.msg) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: json.detail
                    })
                } else {
                    this.props.next()
                    this.props.setMeta('email', this.state.email)
                    this.props.setMeta('code', this.state.code)
                }
            })
            .catch(() => Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong'
            }))
        }

        const onClickNext = () => {
            verifyConfirmationCodeAPI()
        }

        const sendNewCode = () => {
            this.sendConfirmationCodeAPI()
        }

        return (
            <Fragment>
                <div style={styles._wrap}>
                    <div className="welcome_1 screen__center text__center" style={styles.component}>
                        <div className="welcome_1__item text-gray-800" style={styles.item}>
                            <img src={Mobile} alt="wave" style={styles.img} />
                            <p className="op_text">Enter your confirmation code</p>
                        </div>
                        <div><input required value={this.state.code} style={styles.input} onChange={this.setConfirmationCode} /></div>
                        <br />
                        <p className="op_text" style={styles.min_text}>
                            Fill blank with your confirmation code. 
                            <a href="#" onClick={sendNewCode} style={{ color: 'inherit' }} disabled >Send code again</a>
                        </p>
                        <div className="buttons">
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Back" click={this.back} />
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Send" click={onClickNext} />
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

export default EnterPhone
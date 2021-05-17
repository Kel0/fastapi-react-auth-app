import { Component } from 'react'

import Button from '../Button'
import Hand from '../../assets/img/icon_wave.png'

import styles from './Styles'


class Start extends Component {
    render () {
        return (
            <div style={styles._wrap}>
                <div className="welcome_1 screen__center text__center" style={styles.component}>
                    <div className="welcome_1__item text-gray-800" style={styles.item}>
                        <img src={Hand} alt="wave" style={styles.img} className="wave" />
                        <p className="op_text">Clubhouse</p>
                    </div>
                    <p className="op_text">
                        Hey, we're still opening up but anyone can join with an invite from an existing user!
                    </p>
                    <br />

                    <p className="op_text" style={styles.min_text}>
                        Sign up to see if you have friends on Clubhouse who can let you in. We can't wait for you to join!
                    </p>
                    <Button className="btn btn-lg op_text" style={styles.btn} text="Go ahead!" click={this.props.next} />
                </div>
            </div>
        )
    }
}

export default Start
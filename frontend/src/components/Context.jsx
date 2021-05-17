import { Component } from 'react'

import Start from './welcome/Start'
import EnterEmail from './welcome/EnterEmail'
import EnterName from './welcome/EnterName'
import EnterPassword from './welcome/EnterPassword'


class Context extends Component {

    constructor (props) {
        super(props)
        this.state = { step: 0, context: 0, meta: {} }
        this.next = this.next.bind(this)
        this.back = this.back.bind(this)
        this.setMeta = this.setMeta.bind(this)
    }

    next () {
        this.setState({ step: this.state.step + 1 })
    }

    back () {
        this.setState({ step: this.state.step - 1 })
    }

    setMeta(key, value) {
        this.setState(state => {
            state.meta[key] = value
        })
    }

    getNextContext() {
        this.setState({ step: 0, context: this.state.context + 1 })
    }

    _welcome_context() {
        if (this.state.step === 0) return <Start next={this.next} />
        else if (this.state.step === 1) return <EnterName setMeta={this.setMeta} next={this.next} back={this.back} />
        else if (this.state.step === 2) return <EnterEmail meta={this.state.meta} setMeta={this.setMeta} next={this.next} back={this.back} />
        else if (this.state.step === 3) return <EnterPassword meta={this.state.meta} setMeta={this.setMeta} next={this.getNextContext} back={this.back} />
    }

    render () {
        if (this.state.context === 0) return this._welcome_context()
    }
    
}


export default Context
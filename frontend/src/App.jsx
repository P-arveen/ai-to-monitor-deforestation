import React from 'react'
import { Route, Routes } from 'react-router-dom'
import Home from './components/Home'
import Insights from './components/Insights'


const App = () => {
  return (
    <div className='sm:px-20 sm:pt-5 p-10 bg-green-100'>
      <Routes>
        <Route path='/' element={<Home/>} />
        <Route path='/insights' element={<Insights/>}/>

      </Routes>
    </div>
  )
}

export default App

import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import logo from '../assets/logo.png'
import video from '../assets/forest.mp4'
import { useGSAP } from '@gsap/react'
import gsap from 'gsap'
import Deforestationcauses from './Deforestationcauses'
import PredictForm from './PredictForm'
import TemperatureComparison from './TemperatureComparison'


function Home() {

  const [menu, setmenu] = useState(false)

  useGSAP(() => {
    if (menu === true) {
      gsap.to('.menuplate', {
        duration: .5,
        right: '0%'
      })
      gsap.to('.btn', {
        duration: .2,
        onComplete: () => {
          document.querySelector('.btn').classList.add('hidden')
        }
      })
    }
    else {
      gsap.to('.menuplate', {
        duration: .5,
        right: '-100%'
      })
      gsap.to('.btn', {
        duration: .2,
        onComplete: () => {
          document.querySelector('.btn').classList.remove('hidden')
        }
      })
    }


  }, [menu])


  const menuHandler = () => {
    setmenu(true)
    console.log(menu)
  }
  return (
    <div className='w-full h-fit relative overflow-hidden'>
      <div className="navbar border-b-[1px] border-green-900">
        <div className=' flex justify-between  pr-5 items-center md:text-lg  text-sm gap-10 md:gap-20'>
          <div className="logo">
            <img className='md:w-40 w-30' src={logo} alt="" />
          </div>
          <i onClick={() => menuHandler()} className="btn sm:hidden block ri-menu-fold-3-line text-green-700 text-3xl"></i>
          <div className='menuplate sm:flex-row flex-col sm:text-xl text-2xl items-center sm:pt-0 pt-10  flex gap-5 sm:static z-40 absolute h-full sm:w-fit bg-white top-0 w-full'>
            <Link className='navitem' to='/' >Home</Link>
            <Link className='navitem' to='/insights' >Insights</Link>
            <Link className='navitem' to='/predictions'>Predictions</Link>
            <i onClick={() => setmenu(false)} className="ri-xrp-line sm:hidden text-3xl"></i>
          </div>
        </div>
      </div>

      <div className='w-full text-center flex items-center justify-center mt-10'>
        <h1 className='sm:text-4xl md:text-5xl text-2xl font-mono text-center  xl:w-1/3  w-1/2 '>AI-Powered Deforestation Monitoring</h1>
      </div>

      <div className='w-full h-full flex items-start pt-20 justify-center '>
        <div className=' relative w-[60%] h-[25vw] overflow-hidden rounded-2xl'>
          <div className='w-full h-full bg-black top-0 left-0 opacity-[0.5] absolute'>
          </div>
          <video className='w-full h-full object-cover' loop autoPlay muted src={video}></video>
        </div>
      </div>

      <p className='text-xl text-justify text-green-700 mt-20'>Forests cover nearly one-third of the land area on our planet and are home to most of the world’s life on land. They are also essential to human health, purifying our water and air and serving as our first line of defense against new infectious diseases. Additionally, forests provide more than 86 million green jobs and resources such as food and fuel that support billions of people’s livelihoods. Forests also play a critical role in mitigating climate change because they act as carbon sinks—soaking up carbon dioxide that would otherwise be free in the atmosphere and contributing to ongoing changes in climate patterns. </p>
      <div>
        <TemperatureComparison/>
        <PredictForm/>
      </div>
      <Deforestationcauses/>
      <p  className='text-xl text-justify text-red-400 mt-20'>Deforestation can result in more carbon dioxide being released into the atmosphere. That is because trees take in carbon dioxide from the air for photosynthesis, and carbon is locked chemically in their wood. When trees are burned, this carbon returns to the atmosphere as carbon dioxide. With fewer trees around to take in the carbon dioxide, this greenhouse gas accumulates in the atmosphere and accelerates global warming.</p>
    </div>
  )
}

export default Home
import React from 'react'
import { Button } from '../components/Button'
import { Label } from '../components/Field'
import { Input } from '../components/Field'


export default function Login() {
  return (
    <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <h1 className="text-4xl font-bold text-white mb-10 text-center">
        Plex-Letterboxd-Sync
      </h1>
      <div className="flex flex-col mb-2">
        <Label>Username</Label>
        <Input className={"focus:outline-none focus:ring-gray-400 focus:ring-2 rounded-sm"}/>
      </div>
      <div className="flex flex-col mb-4">
        <Label >Password</Label>
        <Input className={"focus:outline-none focus:ring-gray-400 focus:ring-2 rounded-sm"}/>
      </div>
      <Button>Login</Button>
    </div>
  )
}

import { ipAddress, next } from '@vercel/edge'
import { Ratelimit } from '@upstash/ratelimit'
import { kv } from '@vercel/kv'

const ratelimit = new Ratelimit({
  redis: kv,
  limiter: Ratelimit.slidingWindow(10, '10 s'),
})

export default async function middleware(request) {
  const ip = ipAddress(request) || '127.0.0.1'
  console.log('IP:', ip)
  const { success, pending, limit, reset, remaining } = await ratelimit.limit(
    ip
  )

  if (success) {
    return next()
  } else {
    console.log('User rate limit exceeded:', { ip, pending, limit, reset, remaining })
    return new Response("Rate limit exceeded. Please reduce your request frequency.", { status: 429 })
  }
}
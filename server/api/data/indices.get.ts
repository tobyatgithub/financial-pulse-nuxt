import { readFile } from 'fs/promises'
import { join } from 'path'

export default defineEventHandler(async () => {
  try {
    const dataPath = join(process.cwd(), 'static/data/indices.json')
    const content = await readFile(dataPath, 'utf-8')
    return JSON.parse(content)
  } catch (error) {
    console.error('Failed to read indices data:', error)
    return { error: 'Failed to load data' }
  }
})

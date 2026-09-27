export type ProjectStatus = 'active' | 'live' | 'archived'

export interface ProjectLink {
  label: string
  href: string
}

export interface ProjectItem {
  /** URL-safe id, also used as the DOM anchor (`/projects#acg`). */
  id: string
  name: string
  tagline: string
  period: string
  status: ProjectStatus
  /** Set on the one project that gets the wide featured card. */
  featured?: boolean
  summary: string
  highlights: string[]
  stack: string[]
  links?: ProjectLink[]
}

import { nextTick, ref } from 'vue'

// html2canvas + jsPDF are ~550 kB minified. Load them only when the user
// actually clicks a download button so the resume page itself stays light.
const loadHtml2Canvas = () => import('html2canvas').then((m) => m.default)
const loadJsPdf = () => import('jspdf').then((m) => m.default)

export function useDownload() {
  const isExporting = ref(false)
  const error = ref<string | null>(null)

  async function captureNodes(nodes: HTMLElement[]): Promise<HTMLCanvasElement[]> {
    const html2canvas = await loadHtml2Canvas()
    const canvases: HTMLCanvasElement[] = []
    for (const node of nodes) {
      const canvas = await html2canvas(node, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
      })
      canvases.push(canvas)
    }
    return canvases
  }

  async function exportPng(nodes: HTMLElement[], baseName = 'resume'): Promise<void> {
    isExporting.value = true
    error.value = null
    try {
      await nextTick()
      const canvases = await captureNodes(nodes)
      canvases.forEach((canvas, idx) => {
        const link = document.createElement('a')
        link.href = canvas.toDataURL('image/png')
        link.download = canvases.length > 1 ? `${baseName}_${idx + 1}.png` : `${baseName}.png`
        link.click()
      })
    } catch (e) {
      error.value = e instanceof Error ? e.message : '輸出失敗'
    } finally {
      isExporting.value = false
    }
  }

  async function exportPdf(nodes: HTMLElement[], baseName = 'resume'): Promise<void> {
    isExporting.value = true
    error.value = null
    try {
      await nextTick()
      const [canvases, jsPDF] = await Promise.all([captureNodes(nodes), loadJsPdf()])
      const pdf = new jsPDF({
        unit: 'mm',
        format: 'a4',
        orientation: 'portrait',
      })
      const pageWidth = pdf.internal.pageSize.getWidth()
      const pageHeight = pdf.internal.pageSize.getHeight()

      canvases.forEach((canvas, idx) => {
        const imgData = canvas.toDataURL('image/png')
        if (idx > 0) pdf.addPage()
        pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, pageHeight)
      })

      pdf.save(`${baseName}.pdf`)
    } catch (e) {
      error.value = e instanceof Error ? e.message : '輸出失敗'
    } finally {
      isExporting.value = false
    }
  }

  function downloadAsset(path: string, filename?: string): void {
    const link = document.createElement('a')
    link.href = path
    if (filename) link.download = filename
    link.click()
  }

  return {
    isExporting,
    error,
    exportPng,
    exportPdf,
    downloadAsset,
  }
}

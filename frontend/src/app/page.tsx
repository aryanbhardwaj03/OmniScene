import Link from "next/link"

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 w-full px-4 text-center">
      <div className="absolute inset-0 -z-10 h-full w-full bg-background bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]">
        <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary opacity-20 blur-[100px]"></div>
      </div>
      
      <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6">
        Intelligent Vision for <br />
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-emerald-400">
          Plants & Beyond
        </span>
      </h1>
      
      <p className="max-w-2xl text-lg text-muted-foreground mb-10">
        OmniScene is a modular AI platform capable of detecting plants, diagnosing diseases, 
        explaining predictions via Grad-CAM, and searching for similar cases instantly.
      </p>

      <div className="flex flex-col sm:flex-row gap-4 mb-16">
        <Link 
          href="/analyze" 
          className="inline-flex h-12 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          Upload & Analyze
        </Link>
        <Link 
          href="/history" 
          className="inline-flex h-12 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          View History
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full text-left">
        <div className="glass-card p-6">
          <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary"><path d="M12 22c4-4 4-10 4-14 0-4-4-4-4-4s-4 0-4 4c0 4 0 10 4 14z"/><path d="M12 22V10"/><path d="M12 14h.01"/></svg>
          </div>
          <h3 className="font-semibold text-xl mb-2">Species & Disease</h3>
          <p className="text-muted-foreground text-sm">Identifies 14 plant species and 38 diseases using fine-tuned EfficientNet models.</p>
        </div>
        
        <div className="glass-card p-6">
          <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary"><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"/><line x1="16" y1="5" x2="22" y2="11"/><line x1="22" y1="5" x2="16" y2="11"/></svg>
          </div>
          <h3 className="font-semibold text-xl mb-2">Explainable AI</h3>
          <p className="text-muted-foreground text-sm">Visualizes model attention using Grad-CAM heatmaps to build trust and verify predictions.</p>
        </div>

        <div className="glass-card p-6">
          <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <h3 className="font-semibold text-xl mb-2">Similarity Search</h3>
          <p className="text-muted-foreground text-sm">Finds visually similar cases instantly using DINOv2 embeddings and FAISS vector indexing.</p>
        </div>
      </div>
    </div>
  )
}

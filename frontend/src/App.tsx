import { useEffect, useState } from "react";
import { Excalidraw } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";

const LOCAL_STORAGE_KEY = "excalidraw_scene";

export default function App() {
  const [excalidrawAPI, setExcalidrawAPI] = useState<any>(null);

  // Load saved scene from localStorage
const loadScene = () => {
  const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
  if (!saved) return null;

  const parsed = JSON.parse(saved);

  // Ensure collaborators is a Map
  return {
    ...parsed,
    appState: {
      ...parsed.appState,
      collaborators: parsed.appState?.collaborators
        ? new Map(Object.entries(parsed.appState.collaborators))
        : new Map(),
    },
  };
};


  useEffect(() => {
    if (!excalidrawAPI) return;

    // Subscribe to changes and save to localStorage
    const unsubscribe = excalidrawAPI.onChange((elements:any, appState:any, files:any) => {
      const fullScene = { elements, appState, files };
      // Save scene to localStorage
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(fullScene));
    });

    return () => unsubscribe();
  }, [excalidrawAPI]);

  return (
    <div style={{ height: "100vh" }}>
      <Excalidraw
        excalidrawAPI={(api) => setExcalidrawAPI(api)}
        initialData={loadScene()} // Load previously saved scene
      />
    </div>
  );
}

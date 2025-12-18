// Custom Hooks for Editor Functionality
const { useEffect, useRef } = React;

window.useQuillEditor = (onTextChange, onTextSelection) => {
  const quillRef = useRef(null);

  useEffect(() => {
    if (!quillRef.current) {
      quillRef.current = new Quill("#editor-container", {
        theme: "snow",
        placeholder: "Soraty eto ny textinao...",
        modules: {
          toolbar: [
            ["bold", "italic", "underline", "strike"],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ header: [1, 2, 3, false] }],
            [{ color: [] }, { background: [] }],
            ["clean"],
          ],
        },
      });

      quillRef.current.on("text-change", () => {
        const content = quillRef.current.getText();
        onTextChange(content);
      });

      quillRef.current.root.addEventListener("mouseup", () => {
        const selection = window.getSelection();
        const word = selection.toString().trim();
        if (word && word.split(" ").length === 1) {
          onTextSelection(word);
        }
      });
    }
  }, [onTextChange, onTextSelection]);

  return quillRef;
};
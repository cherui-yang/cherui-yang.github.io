window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],  // 识别 \(...\) 行内公式
    displayMath: [["$$", "$$"], ["\\[", "\\]"]], // 识别 $$...$$ 或 \[...\] 块级公式
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// 这个函数确保页面在加载或切换时，新内容中的公式能被正确渲染
document$.subscribe(() => { 
  MathJax.typesetPromise()
})


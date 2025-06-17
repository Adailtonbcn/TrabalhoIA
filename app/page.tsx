"use client"

import type React from "react"

import { useState } from "react"
import { Upload, FileText, Brain, Download, Star } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface AnalysisResult {
  overallScore: number
  clarity: {
    score: number
    feedback: string
    suggestions: string[]
  }
  structure: {
    score: number
    feedback: string
    suggestions: string[]
  }
  keywords: {
    score: number
    missing: string[]
    present: string[]
    suggestions: string[]
  }
  improvements: string[]
  strengths: string[]
  summary: string
}

export default function SmartCVAnalyzer() {
  const [file, setFile] = useState<File | null>(null)
  const [content, setContent] = useState("")
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState("")

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (!selectedFile) return

    setFile(selectedFile)
    setError("")

    try {
      let text = ""

      if (selectedFile.type === "text/plain") {
        text = await selectedFile.text()
      } else if (selectedFile.type === "application/pdf") {
        // Simulação de extração de PDF - em produção usaria uma biblioteca como pdf-parse
        text = `[Conteúdo extraído do PDF: ${selectedFile.name}]
        
João Silva
Desenvolvedor Full Stack

EXPERIÊNCIA PROFISSIONAL
• Desenvolvedor Sênior na TechCorp (2020-2024)
  - Desenvolvimento de aplicações web com React e Node.js
  - Liderança de equipe de 5 desenvolvedores
  - Implementação de arquiteturas escaláveis

• Desenvolvedor Júnior na StartupXYZ (2018-2020)
  - Desenvolvimento frontend com JavaScript
  - Manutenção de sistemas legados

FORMAÇÃO
• Bacharelado em Ciência da Computação - UFMG (2014-2018)

HABILIDADES
JavaScript, React, Node.js, Python, SQL, Git`
      }

      setContent(text)
    } catch (err) {
      setError("Erro ao processar o arquivo. Tente novamente.")
    }
  }

  const analyzeCV = async () => {
    if (!content) return

    setIsAnalyzing(true)
    setError("")

    try {
      const response = await fetch("/api/analyze-cv", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      })

      if (!response.ok) {
        throw new Error("Erro na análise")
      }

      const result = await response.json()
      setAnalysis(result)
    } catch (err) {
      setError("Erro ao analisar o currículo. Tente novamente.")
    } finally {
      setIsAnalyzing(false)
    }
  }

  const exportReport = () => {
    if (!analysis) return

    const reportContent = `
RELATÓRIO DE ANÁLISE DE CURRÍCULO - SmartCV

NOTA GERAL: ${analysis.overallScore}/100

=== ANÁLISE DETALHADA ===

CLAREZA E COESÃO (${analysis.clarity.score}/100):
${analysis.clarity.feedback}

Sugestões:
${analysis.clarity.suggestions.map((s) => `• ${s}`).join("\n")}

ESTRUTURA (${analysis.structure.score}/100):
${analysis.structure.feedback}

Sugestões:
${analysis.structure.suggestions.map((s) => `• ${s}`).join("\n")}

PALAVRAS-CHAVE (${analysis.keywords.score}/100):
Palavras-chave encontradas: ${analysis.keywords.present.join(", ")}
Palavras-chave ausentes: ${analysis.keywords.missing.join(", ")}

=== PONTOS FORTES ===
${analysis.strengths.map((s) => `• ${s}`).join("\n")}

=== MELHORIAS SUGERIDAS ===
${analysis.improvements.map((s) => `• ${s}`).join("\n")}

=== RESUMO ===
${analysis.summary}

---
Relatório gerado pelo SmartCV - Analisador de Currículos com IA
    `

    const blob = new Blob([reportContent], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "relatorio-analise-cv.txt"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600"
    if (score >= 60) return "text-yellow-600"
    return "text-red-600"
  }

  const getScoreBadgeVariant = (score: number) => {
    if (score >= 80) return "default"
    if (score >= 60) return "secondary"
    return "destructive"
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Brain className="h-8 w-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">SmartCV</h1>
          </div>
          <p className="text-xl text-gray-600">Analisador de Currículos com Inteligência Artificial</p>
          <p className="text-gray-500 mt-2">Receba feedback detalhado e melhore seu currículo com IA</p>
        </div>

        {/* Upload Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload do Currículo
            </CardTitle>
            <CardDescription>Faça upload do seu currículo em formato PDF ou TXT para análise</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <input type="file" accept=".pdf,.txt" onChange={handleFileUpload} className="hidden" id="file-upload" />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-lg font-medium text-gray-700">Clique para selecionar um arquivo</p>
                  <p className="text-sm text-gray-500">PDF ou TXT (máx. 10MB)</p>
                </label>
              </div>

              {file && (
                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <FileText className="h-5 w-5 text-blue-600" />
                    <span className="font-medium">{file.name}</span>
                    <Badge variant="secondary">{(file.size / 1024).toFixed(1)} KB</Badge>
                  </div>
                  <Button
                    onClick={analyzeCV}
                    disabled={isAnalyzing || !content}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {isAnalyzing ? "Analisando..." : "Analisar Currículo"}
                  </Button>
                </div>
              )}

              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Overall Score */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <Star className="h-5 w-5" />
                    Nota Geral
                  </span>
                  <Badge variant={getScoreBadgeVariant(analysis.overallScore)} className="text-lg px-3 py-1">
                    {analysis.overallScore}/100
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Progress value={analysis.overallScore} className="mb-4" />
                <p className="text-gray-700">{analysis.summary}</p>
              </CardContent>
            </Card>

            {/* Detailed Analysis */}
            <Tabs defaultValue="analysis" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="analysis">Análise Detalhada</TabsTrigger>
                <TabsTrigger value="keywords">Palavras-chave</TabsTrigger>
                <TabsTrigger value="suggestions">Sugestões</TabsTrigger>
                <TabsTrigger value="export">Exportar</TabsTrigger>
              </TabsList>

              <TabsContent value="analysis" className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between text-lg">
                        Clareza e Coesão
                        <span className={`font-bold ${getScoreColor(analysis.clarity.score)}`}>
                          {analysis.clarity.score}/100
                        </span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <Progress value={analysis.clarity.score} className="mb-3" />
                      <p className="text-sm text-gray-700 mb-3">{analysis.clarity.feedback}</p>
                      <div className="space-y-1">
                        {analysis.clarity.suggestions.map((suggestion, index) => (
                          <div key={index} className="text-sm text-blue-700 bg-blue-50 p-2 rounded">
                            • {suggestion}
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between text-lg">
                        Estrutura
                        <span className={`font-bold ${getScoreColor(analysis.structure.score)}`}>
                          {analysis.structure.score}/100
                        </span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <Progress value={analysis.structure.score} className="mb-3" />
                      <p className="text-sm text-gray-700 mb-3">{analysis.structure.feedback}</p>
                      <div className="space-y-1">
                        {analysis.structure.suggestions.map((suggestion, index) => (
                          <div key={index} className="text-sm text-blue-700 bg-blue-50 p-2 rounded">
                            • {suggestion}
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="keywords" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      Análise de Palavras-chave
                      <span className={`font-bold ${getScoreColor(analysis.keywords.score)}`}>
                        {analysis.keywords.score}/100
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <h4 className="font-medium text-green-700 mb-2">Palavras-chave Encontradas:</h4>
                      <div className="flex flex-wrap gap-2">
                        {analysis.keywords.present.map((keyword, index) => (
                          <Badge key={index} variant="default" className="bg-green-100 text-green-800">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h4 className="font-medium text-red-700 mb-2">Palavras-chave Ausentes:</h4>
                      <div className="flex flex-wrap gap-2">
                        {analysis.keywords.missing.map((keyword, index) => (
                          <Badge key={index} variant="destructive" className="bg-red-100 text-red-800">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h4 className="font-medium text-blue-700 mb-2">Sugestões:</h4>
                      <div className="space-y-2">
                        {analysis.keywords.suggestions.map((suggestion, index) => (
                          <div key={index} className="text-sm text-blue-700 bg-blue-50 p-3 rounded">
                            • {suggestion}
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="suggestions" className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-green-700">Pontos Fortes</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {analysis.strengths.map((strength, index) => (
                          <div key={index} className="flex items-start gap-2">
                            <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                            <p className="text-sm text-gray-700">{strength}</p>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-orange-700">Melhorias Sugeridas</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {analysis.improvements.map((improvement, index) => (
                          <div key={index} className="flex items-start gap-2">
                            <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0" />
                            <p className="text-sm text-gray-700">{improvement}</p>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="export">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Download className="h-5 w-5" />
                      Exportar Relatório
                    </CardTitle>
                    <CardDescription>Baixe um relatório completo da análise do seu currículo</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="p-4 bg-gray-50 rounded-lg">
                        <h4 className="font-medium mb-2">O relatório incluirá:</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          <li>• Nota geral e justificativa</li>
                          <li>• Análise detalhada por critério</li>
                          <li>• Lista de pontos fortes identificados</li>
                          <li>• Sugestões específicas de melhoria</li>
                          <li>• Análise de palavras-chave</li>
                        </ul>
                      </div>
                      <Button onClick={exportReport} className="w-full">
                        <Download className="h-4 w-4 mr-2" />
                        Baixar Relatório (TXT)
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 py-8 border-t border-gray-200">
          <p className="text-gray-500">SmartCV - Analisador de Currículos com IA | Desenvolvido com Next.js e OpenAI</p>
        </div>
      </div>
    </div>
  )
}

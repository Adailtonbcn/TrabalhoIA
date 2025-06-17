import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"
import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { content } = await request.json()

    if (!content) {
      return NextResponse.json({ error: "Conteúdo do currículo é obrigatório" }, { status: 400 })
    }

    const { text } = await generateText({
      model: openai("gpt-4o"),
      system: `Você é um especialista em análise de currículos e recursos humanos. Analise o currículo fornecido e retorne uma análise detalhada em formato JSON com a seguinte estrutura:

{
  "overallScore": number (0-100),
  "clarity": {
    "score": number (0-100),
    "feedback": "string com feedback sobre clareza e coesão",
    "suggestions": ["array", "de", "sugestões"]
  },
  "structure": {
    "score": number (0-100),
    "feedback": "string com feedback sobre estrutura",
    "suggestions": ["array", "de", "sugestões"]
  },
  "keywords": {
    "score": number (0-100),
    "missing": ["palavras-chave", "ausentes"],
    "present": ["palavras-chave", "encontradas"],
    "suggestions": ["sugestões", "para", "palavras-chave"]
  },
  "improvements": ["melhorias", "gerais", "sugeridas"],
  "strengths": ["pontos", "fortes", "identificados"],
  "summary": "resumo geral da análise"
}

Critérios de avaliação:
- Clareza: linguagem clara, objetiva, sem erros gramaticais
- Estrutura: organização lógica, seções bem definidas, formatação
- Palavras-chave: termos relevantes para a área, habilidades técnicas
- Experiência: relevância e descrição das experiências
- Formação: adequação da formação à área

Seja específico e construtivo nas sugestões.`,
      prompt: `Analise este currículo e forneça feedback detalhado:

${content}`,
    })

    // Parse the JSON response from the AI
    const analysis = JSON.parse(text)

    return NextResponse.json(analysis)
  } catch (error) {
    console.error("Erro na análise:", error)
    return NextResponse.json({ error: "Erro interno do servidor" }, { status: 500 })
  }
}

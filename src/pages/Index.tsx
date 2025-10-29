import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Loader2, Sparkles, Copy, Check, Download } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useIsMobile } from "@/hooks/use-mobile";

const Index = () => {
  const [inputText, setInputText] = useState("");
  const [correctedText, setCorrectedText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const { toast } = useToast();
  const isMobile = useIsMobile();

  const handleCorrect = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Error",
        description: "Por favor, ingresa algún texto para corregir.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setCorrectedText("");

    try {
      const { data, error } = await supabase.functions.invoke("correct-text", {
        body: { text: inputText },
      });

      if (error) throw error;

      if (data?.error) {
        toast({
          title: "Error",
          description: data.error,
          variant: "destructive",
        });
        return;
      }

      setCorrectedText(data.correctedText);
      toast({
        title: "¡Texto corregido!",
        description: "Tu texto ha sido corregido exitosamente.",
      });
    } catch (error) {
      console.error("Error correcting text:", error);
      toast({
        title: "Error",
        description: "No se pudo corregir el texto. Intenta nuevamente.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!correctedText) return;
    
    await navigator.clipboard.writeText(correctedText);
    setIsCopied(true);
    toast({
      title: "¡Copiado!",
      description: "Texto copiado al portapapeles.",
    });
    
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleDownload = () => {
    // Descargar el archivo main.py
    const link = document.createElement('a');
    link.href = '/main.py';
    link.download = 'main.py';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast({
      title: "¡Descargando!",
      description: "El archivo main.py se está descargando.",
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/30 to-accent/30">
      <div className="container mx-auto px-4 py-8 md:py-16">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Theme Toggle and Download Button */}
          <div className="flex justify-end items-center gap-3">
            {isMobile && (
              <Button
                variant="outline"
                size="icon"
                onClick={handleDownload}
                className="rounded-full"
              >
                <Download className="h-5 w-5" />
                <span className="sr-only">Descargar versión Python</span>
              </Button>
            )}
            <ThemeToggle />
          </div>
          
          {/* Header */}
          <div className="text-center space-y-4">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 mb-4">
              <Sparkles className="w-8 h-8 text-primary" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
              AI Text Corrector
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Corrige la gramática y sintaxis de tus textos en español con inteligencia artificial
            </p>
          </div>

          {/* Input Card */}
          <Card className="shadow-lg border-border/50">
            <CardHeader>
              <CardTitle>Texto Original</CardTitle>
              <CardDescription>
                Ingresa el texto que deseas corregir
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Escribe o pega tu texto aquí..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="min-h-[200px] resize-none text-base"
              />
              <Button
                onClick={handleCorrect}
                disabled={isLoading || !inputText.trim()}
                className="w-full md:w-auto"
                size="lg"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Corrigiendo...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    Corregir Texto
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Output Card */}
          {correctedText && (
            <Card className="shadow-lg border-primary/20 bg-gradient-to-br from-card to-accent/10 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-primary">Texto Corregido</CardTitle>
                    <CardDescription>
                      Resultado de la corrección con IA
                    </CardDescription>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleCopy}
                    className="ml-4"
                  >
                    {isCopied ? (
                      <>
                        <Check className="w-4 h-4 mr-2" />
                        Copiado
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4 mr-2" />
                        Copiar
                      </>
                    )}
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="rounded-lg bg-card p-4 border border-border/50">
                  <p className="text-base leading-relaxed whitespace-pre-wrap">
                    {correctedText}
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default Index;

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/services/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Article } from "@/schemas/article";
import { toast } from "sonner";

const SubmissionTable = () => {
  const queryClient = useQueryClient();
  const { data: articles, isLoading } = useQuery<Article[]>({
    queryKey: ["admin", "articles"],
    queryFn: () => api.get("/admin/articles").then((res) => res.data),
  });

  const mutation = useMutation({
    mutationFn: ({
      articleId,
      status,
    }: {
      articleId: number;
      status: string;
    }) => {
      return api.put(`/admin/articles/${articleId}/status`, { status });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "articles"] });
      toast.success("وضعیت مقاله با موفقیت تغییر کرد");
    },
    onError: () => {
      toast.error("خطا در تغییر وضعیت مقاله");
    },
  });

  if (isLoading) return <div>در حال بارگذاری...</div>;

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>عنوان مقاله</TableHead>
          <TableHead>نویسنده</TableHead>
          <TableHead>فایل</TableHead>
          <TableHead>وضعیت</TableHead>
          <TableHead>عملیات</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {articles?.map((article) => (
          <TableRow key={article.id}>
            <TableCell>{article.title}</TableCell>
            <TableCell>{article.author.full_name}</TableCell>
            <TableCell>
              {article.file_path && (
                <a
                  href={`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/${article.file_path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline"
                >
                  دانلود
                </a>
              )}
            </TableCell>
            <TableCell>
              <Badge>{article.status}</Badge>
            </TableCell>
            <TableCell>
              <Button
                size="sm"
                onClick={() =>
                  mutation.mutate({
                    articleId: article.id,
                    status: "approved",
                  })
                }
              >
                تایید
              </Button>
              <Button
                variant="destructive"
                size="sm"
                className="mr-2"
                onClick={() =>
                  mutation.mutate({
                    articleId: article.id,
                    status: "rejected",
                  })
                }
              >
                رد
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default SubmissionTable;

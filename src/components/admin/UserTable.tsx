import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/services/api";
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
import { User } from "@/schemas/user";
import { toast } from "sonner";

const UserTable = () => {
  const queryClient = useQueryClient();
  const { data: users, isLoading } = useQuery<User[]>({
    queryKey: ["admin", "users"],
    queryFn: () => api.get("/admin/users").then((res) => res.data),
  });

  const mutation = useMutation({
    mutationFn: ({
      userId,
      isActive,
    }: {
      userId: number;
      isActive: boolean;
    }) => {
      return api.put(`/admin/users/${userId}/status`, { is_active: isActive });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      toast.success("وضعیت کاربر با موفقیت تغییر کرد");
    },
    onError: () => {
      toast.error("خطا در تغییر وضعیت کاربر");
    },
  });

  if (isLoading) return <div>در حال بارگذاری...</div>;

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>نام کامل</TableHead>
          <TableHead>ایمیل</TableHead>
          <TableHead>وضعیت</TableHead>
          <TableHead>عملیات</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {users?.map((user) => (
          <TableRow key={user.id}>
            <TableCell>{user.full_name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>
              <Badge variant={user.is_active ? "default" : "destructive"}>
                {user.is_active ? "فعال" : "غیرفعال"}
              </Badge>
            </TableCell>
            <TableCell>
              <Button
                size="sm"
                onClick={() =>
                  mutation.mutate({ userId: user.id, isActive: true })
                }
              >
                فعال کردن
              </Button>
              <Button
                variant="destructive"
                size="sm"
                className="mr-2"
                onClick={() =>
                  mutation.mutate({ userId: user.id, isActive: false })
                }
              >
                غیرفعال کردن
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default UserTable;

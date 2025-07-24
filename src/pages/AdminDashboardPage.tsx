import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import SubmissionTable from "@/components/admin/SubmissionTable";
import UserTable from "@/components/admin/UserTable";

const AdminDashboardPage = () => {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">پنل مدیریت</h1>
      <Tabs defaultValue="submissions">
        <TabsList>
          <TabsTrigger value="submissions">مقالات</TabsTrigger>
          <TabsTrigger value="users">کاربران</TabsTrigger>
        </TabsList>
        <TabsContent value="submissions">
          <SubmissionTable />
        </TabsContent>
        <TabsContent value="users">
          <UserTable />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdminDashboardPage;

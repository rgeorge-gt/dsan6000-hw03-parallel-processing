# DSAN 6000 Homework 3: Map Reduce for Parallel Processing

**Due Friday, September 25, 5:59pm EDT**

> [!WARNING]
> If you have cloned the repository **template** from the `https://github.com/jpowerj/dsan6000-hw03-parallel-processing` URL, you are **not starting the assignment correctly!** That is, if the command you used to clone the repo onto EC2 looks like:
> 
> `git clone https://github.com/jpowerj/dsan6000-hw03-parallel-processing`
> 
> This will **not work** for assignments in this course, since you **will not be able to push your changes** back to this repository! (Notice how the above code purposefully has *no copy button!*) Instead, you need to create your **own *private* version of the template** (shared with instructors only), as described in the next section.

### Creating Your Own *Private* Repo From the Template

Click the **green "Use this template" button** in the upper-right corner of the template repo on GitHub, then choose the "Create a new repository" option. On the next page, you will be able to create a **new repository** in **your own GitHub account**. Follow these steps to set up your new private repository:

1.  Within the **"1. General"** section, call it **`dsan6000-hw03-parallel-processing`** (the same name as the template), and
1.  Within the **"2. Configuration"** section, choose **Private**
1.  Click the green **Create Repository** button
1.  Once the repository has been created, open the **Settings** page linked at the top of the GitHub interface
1.  In the menu on the left side of the Settings page, within the **"Access"** section, click **"Collaborators"**
1.  Use the **"Manage access"** portion of this Collaborators page to add the course instructors via our GitHub usernames, given in the following table:

<table>
<thead>
</thead>
<tbody>
<tr>
<td>Jeff</td>
<td>
  
```
jpowerj
```

</td>
</tr>
<tr>
<td>Samyu</td>
<td>

```
samyu-vakkalanka
```

</td>
</tr>
<tr>
<td>Fangzhou</td>
<td>

```
fangzhou-wang
```

</td>
</tr>
<tr>
<td>Siru</td>
<td>

```
siruwuu
```

</td>
</tr>
</tbody>
</table>

Once this **derived** private repository has been set up on **your GitHub account**, and you have added the instructors as collaborators, you are all set up to **submit the URL for your newly-created repository on Canvas!** Please submit the URL immediately after creating the repo: this is what will allow us to see your progress and check any issues between distribution and submission.

Then, once you have submitted the URL on Canvas, **clone *your* newly-created repository (*not* the template owned by `jpowerj`) to your EC2 instance to begin working!** In other words, the command you run on EC2 should look as follows (with your GitHub username in place of `YOUR_GH_USERNAME`):

```bash
git clone https://github.com/YOUR_GH_USERNAME/dsan6000-hw03-parallel-processing
```

Note that this and other `git` commands interacting with your GitHub repository will likely require you to use a GitHub **Access Token** in place of your password (despite the fact that `git` will ask you for your password, the password you use to log into your GitHub account in your browser typically will *not* work within the `git` command-line interface).

To create this Access Token, **follow the instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)**: you can just check off all permissions (since this is a case of you "granting" permissions to yourself – you would need to worry about specific permissions if you were granting access to a coworker on a project, for example!), and you don't need to choose an expiration date for this Access Token (though you can for extra account security).

## HW3 Task: Utilizing `joblib` and `MRJob` to Process Data in Parallel

Now that you are set up on EC2 (after completing HW1), and now that you have connected to your EC2 instance to develop in Python using Jupyter notebooks (after completing HW2), the workflow for homeworks from now onwards should now feel more familiar! Setting up your `uv` environment for this homework works the same as the previous homework, with `hw03` replacing `hw02`:

> [!NOTE]
> ### Setting Up `uv`
> 
> In this class, to ensure that the Python libraries necessary for each assignment are installed on your EC2 instance, we will be using the [`uv` package manager](https://docs.astral.sh/uv/). Setting up `uv` and then activating the environment works as follows:
> 
> 1.  If you have not yet installed `uv` on your EC2 instance, run the following command within VSCode's Integrated Terminal:
> 
>     ```bash
>     curl -LsSf https://astral.sh/uv/install.sh | sh
>     ```
> 2.  Now, within the cloned homework directory, just type `uv sync`, and `uv` will create a new Python environment (within a subdirectory it will create, called `.venv`) where all libraries necessary for this assignment are automatically installed.
> 3.  Once the `uv sync` command has finished running, activate the created environment by executing
> 
>     ```
>     source .venv/bin/activate`
>     ```
> 4. If the environment was activated successfully, the command prompt in VSCode's Integrated Terminal should now have a `(dsan6000-hw03)` prefix. That is, the prompt should look like:
> 
>     ```bash
>     (dsan6000-hw03) ubuntu@ip-172-31-78-63:~/dsan6000-hw03$ 
>     ```
>     
>     Instead of
>     
>     ```
>     ubuntu@ip-172-31-78-63:~/dsan6000-hw03$ 
>     ```
> 
> 5.  What we've done thus far means that you could now run "plain" `.py` files, and the necessary libraries would be ready for use. However, since we want to utilize **Jupyter notebooks** to write our code, we need to register this environment as a **kernel** that Jupyter can use to execute the code you write within Jupyter notebook code cells. To achieve this, we'll need the `ipykernel` library, which you should now install within your `uv` environment by executing the following command:
> 
>     ```bash
>     uv pip install ipykernel
>     ```
> 
> 6.  Once `ipykernel` has been installed within your `uv` environment, the final step is to **register** this `uv` environment with Jupyter, so that it can be chosen as your desired environment within Jupyter (rather than the default "base" Python environment). To achieve this, execute the following command:
> 
>     ```bash
>     python -m ipykernel install --user --name=hw03-kernel
>     ```
> 7. Once this command has executed successfully, your assignment-specific `uv` environment is now ready for use as a Jupyter kernel! Unfortunately, the only way to get VSCode to detect this new kernel (so that it appears as an option when you choose the kernel for a Jupyter notebook) is by reloading VSCode. But, rather than closing the window and reconnecting, there's an easier approach! Oen the VSCode **Command Palette** using `Ctrl+Shift+P`, then start typing "Reload". You should see the full set of commands filter as you type, leaving the option **"Developer: Reload Window"** near the top. Click this command and your window should reload in the same state, but now with your kernel detected by VSCode.

The remaining instructions are given in two notebooks:

* In `DSAN6000_HW3A.ipynb` you will use `joblib` to handle distributing the subtasks of an "embarrassingly-parallel" problem to the cores of your EC2 instance
* In `DSAN6000_HW3B.ipynb` you will use `MRJob` to **"factor"** a *non-*embarrassingly-parallel problem into a series of embarrassingly-parallel subtasks, distribute these subtasks to the cores of your EC2 instance, and then **re-combine** the subtask results into a solution to the original problem.

## HW3 Submission

Since you submitted your GitHub URL all the way up at the top of the instructions, all that is left is for you to **push your work from EC2 to GitHub**. If you push a commit with the commit message **"Final submission"** (by running `git commit -m "Final submission"` and then `git push`), we will consider your repo ready to grade – otherwise, if no commit with this message is found, we will consider the **most recent commit when the due date is reached** to be your final submission.

---

Assignment hash (SHA-256): `264698182a8abe8f4b6a89f898c9021055665e930cea90c338b9d986fe61445a`
